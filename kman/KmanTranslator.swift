import Foundation
import Translation

struct Piece: Codable {
    let text: String
    let translate: Bool
}

struct Item: Codable {
    let pieces: [Piece]
}

struct TranslationInput: Codable {
    let source: String
    let target: String
    let items: [Item]
}

struct TranslationOutput: Codable {
    let translations: [String]
}

enum TranslatorFailure: Error, LocalizedError {
    case invalidArguments
    case languageModelNotInstalled
    case missingResponse(String)

    var errorDescription: String? {
        switch self {
        case .invalidArguments:
            return "입력 파일과 출력 파일 경로가 필요합니다."
        case .languageModelNotInstalled:
            return "영어-한국어 Apple 번역 언어 모델이 설치되어 있지 않습니다."
        case .missingResponse(let identifier):
            return "번역 응답이 누락되었습니다: \(identifier)"
        }
    }
}

@main
struct KmanTranslator {
    static func main() async {
        do {
            guard CommandLine.arguments.count == 3 else {
                throw TranslatorFailure.invalidArguments
            }

            let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
            let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
            let payload = try JSONDecoder().decode(
                TranslationInput.self,
                from: Data(contentsOf: inputURL)
            )
            let source = Locale.Language(identifier: payload.source)
            let target = Locale.Language(identifier: payload.target)
            let availability = await LanguageAvailability().status(from: source, to: target)
            guard availability == .installed else {
                throw TranslatorFailure.languageModelNotInstalled
            }

            let session = TranslationSession(
                installedSource: source,
                target: target,
                preferredStrategy: .lowLatency
            )
            var requests: [TranslationSession.Request] = []
            for (index, item) in payload.items.enumerated() {
                var sourceText = AttributedString()
                for piece in item.pieces {
                    var attributedPiece = AttributedString(piece.text)
                    if !piece.translate {
                        attributedPiece.translation.skipsTranslation = true
                    }
                    sourceText.append(attributedPiece)
                }
                requests.append(
                    TranslationSession.Request(
                        sourceText: sourceText,
                        clientIdentifier: String(index)
                    )
                )
            }

            let responses = try await session.translations(from: requests)
            let indexed = Dictionary(
                uniqueKeysWithValues: responses.compactMap { response in
                    response.clientIdentifier.map { ($0, response.targetText) }
                }
            )
            let translations = try payload.items.indices.map { index in
                let identifier = String(index)
                guard let translated = indexed[identifier] else {
                    throw TranslatorFailure.missingResponse(identifier)
                }
                return translated
            }
            let output = TranslationOutput(translations: translations)
            let data = try JSONEncoder().encode(output)
            try data.write(to: outputURL, options: .atomic)
        } catch {
            let message = error.localizedDescription + "\n"
            FileHandle.standardError.write(Data(message.utf8))
            exit(1)
        }
    }
}
