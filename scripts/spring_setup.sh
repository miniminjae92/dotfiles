#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="app.log"
PID_FILE="app.pid"

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

echo "Java 21 Amazon Corretto 설치 중..."

sudo apt-get update
sudo apt-get install -y wget gnupg git

if [ ! -f /usr/share/keyrings/corretto-keyring.gpg ]; then
  wget -O - https://apt.corretto.aws/corretto.key \
    | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg
fi

echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" \
  | sudo tee /etc/apt/sources.list.d/corretto.list > /dev/null

sudo apt-get update
sudo apt-get install -y java-21-amazon-corretto-jdk

echo "Repository clone 중..."
echo "Repository: $REPO_URL"

if [ -n "$BRANCH" ]; then
  echo "Branch: $BRANCH"
fi

if [ -d "$REPO_NAME" ]; then
  echo "기존 $REPO_NAME 디렉토리가 있어 삭제 후 다시 clone 합니다."
  rm -rf "$REPO_NAME"
fi

if [ -n "$BRANCH" ]; then
  git clone -b "$BRANCH" "$REPO_URL" "$REPO_NAME"
else
  git clone "$REPO_URL" "$REPO_NAME"
fi

cd "$REPO_NAME"

echo "Spring Boot 애플리케이션 빌드 중..."

chmod +x ./gradlew
./gradlew bootJar

JAR_FILE=$(find build/libs -name "*.jar" ! -name "*plain.jar" | head -n 1)

if [ -z "$JAR_FILE" ]; then
  echo "실행 가능한 JAR 파일을 찾을 수 없습니다."
  exit 1
fi

echo "JAR 파일: $JAR_FILE"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "이미 애플리케이션이 실행 중입니다. PID: $(cat "$PID_FILE")"
else
  echo "애플리케이션 실행 중..."
  nohup java -jar "$JAR_FILE" >> "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  echo "실행 완료. PID: $(cat "$PID_FILE")"
fi

echo "로그 출력 시작: Ctrl + C를 눌러도 서버는 계속 실행됩니다."
tail -f "$LOG_FILE"
