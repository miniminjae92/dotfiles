import AppKit
import Foundation

private struct Snapshot: Decodable {
    struct Counts: Decodable {
        let pending: Int
        let permissionRequests: Int
        let attention: Int
        let complete: Int

        enum CodingKeys: String, CodingKey {
            case pending
            case permissionRequests = "permission_requests"
            case attention
            case complete
        }
    }

    struct Mode: Decodable {
        let name: String
        let local: String
        let slack: String
        let until: String?
        let next: String?
    }

    struct Event: Decodable {
        let id: String
        let source: String
        let sourceLabel: String
        let status: String
        let kind: String?
        let project: String
        let createdAt: String
        let escalated: Bool
        let canOpen: Bool

        enum CodingKeys: String, CodingKey {
            case id, source, status, kind, project, escalated
            case sourceLabel = "source_label"
            case createdAt = "created_at"
            case canOpen = "can_open"
        }
    }

    let counts: Counts
    let mode: Mode
    let events: [Event]
}

private final class AgentNotifyClient {
    private var executable: String {
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        let installed = "\(home)/.local/bin/agent-notify"
        return FileManager.default.isExecutableFile(atPath: installed)
            ? installed
            : "\(home)/.dotfiles/bin/agent-notify"
    }

    func run(_ arguments: [String]) throws -> Data {
        let process = Process()
        let output = Pipe()
        let errors = Pipe()
        process.executableURL = URL(fileURLWithPath: executable)
        process.arguments = arguments
        process.standardOutput = output
        process.standardError = errors
        try process.run()
        process.waitUntilExit()
        let data = output.fileHandleForReading.readDataToEndOfFile()
        if process.terminationStatus != 0 {
            let message = String(
                data: errors.fileHandleForReading.readDataToEndOfFile(),
                encoding: .utf8
            )?.trimmingCharacters(in: .whitespacesAndNewlines)
            throw NSError(
                domain: "AgentNotifyMenu",
                code: Int(process.terminationStatus),
                userInfo: [NSLocalizedDescriptionKey: message ?? "agent-notify 명령 실패"]
            )
        }
        return data
    }

    func snapshot() throws -> Snapshot {
        try JSONDecoder().decode(Snapshot.self, from: run(["status", "--json"]))
    }
}

private final class AppDelegate: NSObject, NSApplicationDelegate, NSMenuDelegate {
    private let client = AgentNotifyClient()
    private let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    private let menu = NSMenu()
    private var snapshot: Snapshot?
    private var timer: Timer?
    private var refreshInFlight = false
    private var lastError: String?
    private var menuOpen = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        menu.delegate = self
        statusItem.menu = menu
        statusItem.button?.toolTip = "agent-notify"
        updateStatusItem()
        refresh()
        timer = Timer.scheduledTimer(
            timeInterval: 3,
            target: self,
            selector: #selector(refresh),
            userInfo: nil,
            repeats: true
        )
    }

    func applicationWillTerminate(_ notification: Notification) {
        timer?.invalidate()
    }

    func menuNeedsUpdate(_ menu: NSMenu) {
        rebuildMenu()
        refresh()
    }

    func menuWillOpen(_ menu: NSMenu) {
        menuOpen = true
    }

    func menuDidClose(_ menu: NSMenu) {
        menuOpen = false
    }

    @objc private func refresh() {
        guard !refreshInFlight else { return }
        refreshInFlight = true
        DispatchQueue.global(qos: .utility).async { [weak self] in
            guard let self else { return }
            do {
                let value = try self.client.snapshot()
                DispatchQueue.main.async {
                    self.snapshot = value
                    self.lastError = nil
                    self.refreshInFlight = false
                    self.updateStatusItem()
                    if self.menuOpen { self.rebuildMenu() }
                }
            } catch {
                DispatchQueue.main.async {
                    self.lastError = error.localizedDescription
                    self.refreshInFlight = false
                    self.updateStatusItem()
                    if self.menuOpen { self.rebuildMenu() }
                }
            }
        }
    }

    private func updateStatusItem() {
        guard let button = statusItem.button else { return }
        let symbol: String
        let count: Int
        if lastError != nil {
            symbol = "exclamationmark.octagon.fill"
            count = 0
        } else if let snapshot, snapshot.counts.permissionRequests > 0 {
            symbol = "exclamationmark.triangle.fill"
            count = snapshot.counts.permissionRequests
        } else if let snapshot, snapshot.counts.attention > 0 {
            symbol = "exclamationmark.circle.fill"
            count = snapshot.counts.attention
        } else if let snapshot, snapshot.counts.pending > 0 {
            symbol = "checkmark.circle"
            count = snapshot.counts.pending
        } else {
            symbol = "circle.dotted"
            count = 0
        }
        button.image = NSImage(systemSymbolName: symbol, accessibilityDescription: "agent-notify")
        button.image?.isTemplate = true
        button.title = count > 0 ? " \(count)" : ""
        button.toolTip = statusTooltip()
    }

    private func statusTooltip() -> String {
        if let lastError { return "agent-notify 오류: \(lastError)" }
        guard let snapshot else { return "agent-notify 상태 읽는 중" }
        return "승인 \(snapshot.counts.permissionRequests) · 주의 \(snapshot.counts.attention) · 완료 \(snapshot.counts.complete)"
    }

    private func rebuildMenu() {
        menu.removeAllItems()
        guard let snapshot else {
            addDisabled(lastError.map { "오류: \($0)" } ?? "상태 읽는 중…")
            addCommonFooter()
            return
        }

        addDisabled(
            "승인 \(snapshot.counts.permissionRequests) · 주의 \(snapshot.counts.attention) · 완료 \(snapshot.counts.complete)"
        )
        menu.addItem(.separator())

        if snapshot.events.isEmpty {
            addDisabled("대기 중인 이벤트가 없습니다")
        } else {
            for event in snapshot.events.prefix(15) {
                menu.addItem(eventMenuItem(event))
            }
            if snapshot.events.count > 15 {
                addDisabled("외 \(snapshot.events.count - 15)건")
            }
        }

        menu.addItem(.separator())
        menu.addItem(modeMenuItem(snapshot.mode))

        if snapshot.counts.complete > 0 {
            menu.addItem(
                actionItem(
                    "완료 모두 확인",
                    action: #selector(acknowledgeCompleted)
                )
            )
        }
        if snapshot.counts.pending > 0 {
            menu.addItem(
                actionItem(
                    "전체 확인 (승인 대기 포함)…",
                    action: #selector(confirmAcknowledgeAll)
                )
            )
        }
        addCommonFooter()
    }

    private func eventMenuItem(_ event: Snapshot.Event) -> NSMenuItem {
        let prefix: String
        if event.kind == "permission_request" {
            prefix = "승인"
        } else if event.status == "error" {
            prefix = "오류"
        } else if event.status == "attention" {
            prefix = "주의"
        } else {
            prefix = "완료"
        }
        let item = NSMenuItem(
            title: "\(prefix) · \(event.sourceLabel) · \(event.project) · \(relativeAge(event.createdAt))",
            action: nil,
            keyEquivalent: ""
        )
        let submenu = NSMenu()
        let open = actionItem("터미널로 이동", action: #selector(openEvent(_:)))
        open.representedObject = event.id
        open.isEnabled = event.canOpen
        submenu.addItem(open)
        let acknowledge = actionItem("확인", action: #selector(acknowledgeEvent(_:)))
        acknowledge.representedObject = event.id
        submenu.addItem(acknowledge)
        item.submenu = submenu
        return item
    }

    private func modeMenuItem(_ mode: Snapshot.Mode) -> NSMenuItem {
        let root = NSMenuItem(
            title: "전달 mode · local \(mode.local) · Slack \(mode.slack)",
            action: nil,
            keyEquivalent: ""
        )
        let submenu = NSMenu()

        let local = NSMenuItem(title: "Mac 알림", action: nil, keyEquivalent: "")
        let localMenu = NSMenu()
        for value in ["off", "temporary", "persistent"] {
            let item = actionItem(localLabel(value), action: #selector(setLocalMode(_:)))
            item.representedObject = value
            item.state = mode.local == value ? .on : .off
            localMenu.addItem(item)
        }
        local.submenu = localMenu
        submenu.addItem(local)

        let slack = NSMenuItem(title: "Slack", action: nil, keyEquivalent: "")
        let slackMenu = NSMenu()
        for value in ["off", "delayed", "immediate"] {
            let item = actionItem(slackLabel(value), action: #selector(setSlackMode(_:)))
            item.representedObject = value
            item.state = mode.slack == value ? .on : .off
            slackMenu.addItem(item)
        }
        slack.submenu = slackMenu
        submenu.addItem(slack)
        root.submenu = submenu
        return root
    }

    private func addCommonFooter() {
        menu.addItem(.separator())
        menu.addItem(actionItem("새로고침", action: #selector(refresh)))
        menu.addItem(actionItem("agent-notify 종료", action: #selector(quit)))
    }

    private func addDisabled(_ title: String) {
        let item = NSMenuItem(title: title, action: nil, keyEquivalent: "")
        item.isEnabled = false
        menu.addItem(item)
    }

    private func actionItem(_ title: String, action: Selector) -> NSMenuItem {
        let item = NSMenuItem(title: title, action: action, keyEquivalent: "")
        item.target = self
        return item
    }

    @objc private func openEvent(_ sender: NSMenuItem) {
        guard let id = sender.representedObject as? String else { return }
        execute(["open", id])
    }

    @objc private func acknowledgeEvent(_ sender: NSMenuItem) {
        guard let id = sender.representedObject as? String else { return }
        execute(["ack", id])
    }

    @objc private func acknowledgeCompleted() {
        execute(["ack", "--completed"])
    }

    @objc private func confirmAcknowledgeAll() {
        let alert = NSAlert()
        alert.messageText = "승인 대기를 포함한 모든 이벤트를 확인 처리할까요?"
        alert.informativeText = "아직 응답하지 않은 승인 요청도 목록에서 사라집니다."
        alert.addButton(withTitle: "전체 확인")
        alert.addButton(withTitle: "취소")
        NSApp.activate(ignoringOtherApps: true)
        if alert.runModal() == .alertFirstButtonReturn {
            execute(["ack", "--all"])
        }
    }

    @objc private func setLocalMode(_ sender: NSMenuItem) {
        guard
            let value = sender.representedObject as? String,
            let mode = snapshot?.mode
        else { return }
        execute(["mode", "set", "--local", value, "--slack", mode.slack])
    }

    @objc private func setSlackMode(_ sender: NSMenuItem) {
        guard
            let value = sender.representedObject as? String,
            let mode = snapshot?.mode
        else { return }
        execute(["mode", "set", "--local", mode.local, "--slack", value])
    }

    private func execute(_ arguments: [String]) {
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self else { return }
            do {
                _ = try self.client.run(arguments)
                DispatchQueue.main.async { self.refresh() }
            } catch {
                DispatchQueue.main.async {
                    self.lastError = error.localizedDescription
                    self.updateStatusItem()
                    self.rebuildMenu()
                }
            }
        }
    }

    @objc private func quit() {
        NSApp.terminate(nil)
    }

    private func localLabel(_ value: String) -> String {
        ["off": "끔", "temporary": "임시", "persistent": "유지"][value] ?? value
    }

    private func slackLabel(_ value: String) -> String {
        ["off": "끔", "delayed": "지연", "immediate": "즉시"][value] ?? value
    }

    private func relativeAge(_ value: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: value) else { return value }
        let seconds = max(0, Int(Date().timeIntervalSince(date)))
        if seconds < 60 { return "방금" }
        if seconds < 3600 { return "\(seconds / 60)분" }
        if seconds < 86_400 { return "\(seconds / 3600)시간" }
        return "\(seconds / 86_400)일"
    }
}

private func runCheck() -> Int32 {
    do {
        let snapshot = try AgentNotifyClient().snapshot()
        print(
            "pending=\(snapshot.counts.pending) permission_requests=\(snapshot.counts.permissionRequests) local=\(snapshot.mode.local) slack=\(snapshot.mode.slack)"
        )
        return 0
    } catch {
        fputs("AgentNotifyMenu: \(error.localizedDescription)\n", stderr)
        return 1
    }
}

if CommandLine.arguments.contains("--check") {
    exit(runCheck())
}

let application = NSApplication.shared
private let delegate = AppDelegate()
application.delegate = delegate
application.run()
