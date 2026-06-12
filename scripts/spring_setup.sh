#!/usr/bin/env bash
set -euo pipefail

APP_BASE_DIR="$HOME/apps"
LOG_DIR="$HOME/logs"
PID_DIR="$HOME/pids"

mkdir -p "$APP_BASE_DIR" "$LOG_DIR" "$PID_DIR"

install_packages_if_needed() {
  local packages=("$@")
  local missing=()

  for package in "${packages[@]}"; do
    if ! dpkg -s "$package" >/dev/null 2>&1; then
      missing+=("$package")
    fi
  done

  if [ "${#missing[@]}" -eq 0 ]; then
    echo "필수 패키지가 이미 설치되어 있습니다."
    return
  fi

  echo "필수 패키지 설치 중: ${missing[*]}"
  sudo apt-get update
  sudo apt-get install -y "${missing[@]}"
}

install_java21_if_needed() {
  if command -v java >/dev/null 2>&1 && java -version 2>&1 | grep -q 'version "21'; then
    echo "Java 21이 이미 설치되어 있습니다."
    return
  fi

  echo "Java 21 Amazon Corretto 설치 중..."

  install_packages_if_needed wget gnupg git

  if [ ! -f /usr/share/keyrings/corretto-keyring.gpg ]; then
    wget -O - https://apt.corretto.aws/corretto.key \
      | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg
  fi

  if [ ! -f /etc/apt/sources.list.d/corretto.list ]; then
    echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" \
      | sudo tee /etc/apt/sources.list.d/corretto.list > /dev/null

    sudo apt-get update
  fi

  sudo apt-get install -y java-21-amazon-corretto-jdk
}

read -rp "GitHub Repository URL을 입력하세요: " INPUT_URL

if [ -z "$INPUT_URL" ]; then
  echo "Repository URL이 비어 있습니다."
  exit 1
fi

INPUT_URL="${INPUT_URL%/}"
REPO_URL="$INPUT_URL"
BRANCH=""

# GitHub branch URL 형식 지원:
# https://github.com/{owner}/{repo}/tree/{branch}
if [[ "$INPUT_URL" =~ ^https://github.com/([^/]+)/([^/]+)/tree/(.+)$ ]]; then
  OWNER="${BASH_REMATCH[1]}"
  REPO="${BASH_REMATCH[2]}"
  BRANCH="${BASH_REMATCH[3]}"
  REPO_URL="https://github.com/${OWNER}/${REPO}.git"
fi

REPO_NAME=$(basename "$REPO_URL" .git)
APP_DIR="$APP_BASE_DIR/$REPO_NAME"
LOG_FILE="$LOG_DIR/$REPO_NAME.log"
PID_FILE="$PID_DIR/$REPO_NAME.pid"

install_packages_if_needed git
install_java21_if_needed

echo "기존 애플리케이션 확인 중..."

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  OLD_PID=$(cat "$PID_FILE")

  echo "기존 애플리케이션 종료 중. PID: $OLD_PID"
  kill "$OLD_PID"
  sleep 3

  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "정상 종료되지 않아 강제 종료합니다."
    kill -9 "$OLD_PID"
  fi

  rm -f "$PID_FILE"
fi

echo "Repository clone 중..."
echo "Repository: $REPO_URL"

if [ -n "$BRANCH" ]; then
  echo "Branch: $BRANCH"
fi

rm -rf "$APP_DIR"

if [ -n "$BRANCH" ]; then
  git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

echo "Spring Boot 애플리케이션 빌드 중..."

if [ ! -f "./gradlew" ]; then
  echo "gradlew 파일이 없습니다. Gradle Wrapper가 있는 프로젝트만 지원합니다."
  exit 1
fi

chmod +x ./gradlew
./gradlew bootJar

JAR_FILE=$(find build/libs -name "*.jar" ! -name "*plain.jar" | head -n 1)

if [ -z "$JAR_FILE" ]; then
  echo "실행 가능한 JAR 파일을 찾을 수 없습니다."
  exit 1
fi

echo "JAR 파일: $JAR_FILE"
echo "애플리케이션 실행 중..."

nohup java -jar "$JAR_FILE" >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

sleep 2

if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "실행 완료. PID: $(cat "$PID_FILE")"
else
  echo "애플리케이션 실행에 실패했습니다."
  tail -n 50 "$LOG_FILE"
  exit 1
fi

echo "로그 파일: $LOG_FILE"
echo "PID 파일: $PID_FILE"
echo "로그 출력 시작: Ctrl + C를 눌러도 서버는 계속 실행됩니다."

tail -f "$LOG_FILE"
