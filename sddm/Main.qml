// SlackWorld SDDM theme — Qt 6 / QtQuick only, no KDE Frameworks required.
import QtQuick 2.15
import SddmComponents 2.0

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#294f75"

    property int sessionIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
    property string sessionName: qsTr("Session")
    property bool loginPending: false
    property date currentDate: new Date()

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: root.currentDate = new Date()
    }

    function tryLogin() {
        if (username.text.length === 0 || loginPending)
            return
        loginPending = true
        message.color = "#b9cedd"
        message.text = qsTr("Signing in...")
        sddm.login(username.text, password.text, sessionIndex)
    }

    Image {
        anchors.fill: parent
        source: config.stringValue("background")
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        cache: true
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.loginPending = false
            password.text = ""
            message.color = "#ffb4b4"
            message.text = qsTr("Login failed. Check your username and password.")
            password.forceActiveFocus()
        }
        function onInformationMessage(text) {
            message.color = "#b9cedd"
            message.text = text
        }
    }

    Rectangle {
        id: panel
        x: Math.max(72, root.width * 0.075)
        anchors.verticalCenter: parent.verticalCenter
        width: Math.min(570, root.width * 0.42)
        height: 700
        radius: 18
        color: "#d907131f"
        border.width: 2
        border.color: "#9b7b99b0"

        Column {
            anchors.fill: parent
            anchors.margins: 46
            spacing: 16

            Text {
                width: parent.width
                text: config.stringValue("welcomeText")
                color: "#f0f6fa"
                font.family: config.stringValue("fontFamily")
                font.pixelSize: 26
                font.weight: Font.DemiBold
                wrapMode: Text.WordWrap
            }

            Text {
                width: parent.width
                text: qsTr("Sign in to continue")
                color: "#b0c3d1"
                font.family: config.stringValue("fontFamily")
                font.pixelSize: 17
            }

            Item { width: 1; height: 10 }

            Text {
                text: qsTr("USERNAME")
                color: "#91aabd"
                font.family: config.stringValue("fontFamily")
                font.pixelSize: 13
                font.letterSpacing: 1.2
            }

            Rectangle {
                width: parent.width
                height: 52
                radius: 10
                color: username.activeFocus ? "#304e6375" : "#2422384a"
                border.width: 2
                border.color: username.activeFocus ? "#b7d2e5" : "#607f96aa"

                TextInput {
                    id: username
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    verticalAlignment: TextInput.AlignVCenter
                    text: userModel.lastUser
                    color: "#ffffff"
                    selectionColor: "#607f96"
                    selectedTextColor: "#ffffff"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 19
                    selectByMouse: true
                    KeyNavigation.tab: password
                    Keys.onReturnPressed: password.forceActiveFocus()
                    Keys.onEnterPressed: password.forceActiveFocus()
                }
            }

            Text {
                text: qsTr("PASSWORD")
                color: "#91aabd"
                font.family: config.stringValue("fontFamily")
                font.pixelSize: 13
                font.letterSpacing: 1.2
            }

            Rectangle {
                width: parent.width
                height: 52
                radius: 10
                color: password.activeFocus ? "#304e6375" : "#2422384a"
                border.width: 2
                border.color: password.activeFocus ? "#b7d2e5" : "#607f96aa"

                TextInput {
                    id: password
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    verticalAlignment: TextInput.AlignVCenter
                    echoMode: TextInput.Password
                    color: "#ffffff"
                    selectionColor: "#607f96"
                    selectedTextColor: "#ffffff"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 19
                    selectByMouse: true
                    focus: true
                    KeyNavigation.tab: loginButton
                    Keys.onReturnPressed: root.tryLogin()
                    Keys.onEnterPressed: root.tryLogin()
                    Keys.onEscapePressed: text = ""
                }
            }

            Item {
                width: parent.width
                height: 48

                Rectangle {
                    id: sessionButton
                    anchors.left: parent.left
                    width: parent.width * 0.57
                    height: parent.height
                    radius: 9
                    color: sessionMouse.containsMouse ? "#405d768a" : "#3022384a"
                    border.width: 1
                    border.color: "#607f96aa"

                    Text {
                        anchors.left: parent.left
                        anchors.leftMargin: 14
                        anchors.verticalCenter: parent.verticalCenter
                        width: parent.width - 42
                        text: root.sessionName
                        color: "#d5e2eb"
                        elide: Text.ElideRight
                        font.family: config.stringValue("fontFamily")
                        font.pixelSize: 16
                    }
                    Text {
                        anchors.right: parent.right
                        anchors.rightMargin: 14
                        anchors.verticalCenter: parent.verticalCenter
                        text: sessionPopup.visible ? "-" : "+"
                        color: "#d5e2eb"
                        font.pixelSize: 20
                    }
                    MouseArea {
                        id: sessionMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: sessionPopup.visible = !sessionPopup.visible
                    }
                }

                Text {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    visible: keyboard.capsLock
                    text: qsTr("CAPS LOCK")
                    color: "#ffd28a"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }
            }

            Rectangle {
                id: loginButton
                width: parent.width
                height: 54
                radius: 11
                color: loginMouse.pressed ? "#7595ad" : (loginMouse.containsMouse ? "#66869e" : "#587990")
                border.width: 2
                border.color: "#b7d2e5"
                opacity: root.loginPending ? 0.65 : 1.0

                Text {
                    anchors.centerIn: parent
                    text: root.loginPending ? qsTr("PLEASE WAIT") : qsTr("SIGN IN")
                    color: "#ffffff"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 17
                    font.weight: Font.DemiBold
                    font.letterSpacing: 1.1
                }
                MouseArea {
                    id: loginMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.tryLogin()
                }
                Keys.onReturnPressed: root.tryLogin()
                Keys.onEnterPressed: root.tryLogin()
            }

            Text {
                id: message
                width: parent.width
                height: 44
                text: ""
                color: "#b9cedd"
                font.family: config.stringValue("fontFamily")
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Row {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 46
            anchors.rightMargin: 46
            anchors.bottomMargin: 30
            height: 42
            spacing: 12

            Rectangle {
                width: (parent.width - parent.spacing) / 2
                height: parent.height
                radius: 9
                color: rebootMouse.containsMouse && sddm.canReboot ? "#405d768a" : "#3022384a"
                border.width: 1
                border.color: "#607f96aa"
                Text {
                    anchors.centerIn: parent
                    text: qsTr("RESTART")
                    color: "#d5e2eb"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 13
                }
                MouseArea {
                    id: rebootMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: if (sddm.canReboot) sddm.reboot()
                }
            }

            Rectangle {
                width: (parent.width - parent.spacing) / 2
                height: parent.height
                radius: 9
                color: powerMouse.containsMouse && sddm.canPowerOff ? "#754d55" : "#3022384a"
                border.width: 1
                border.color: "#8f6b73"
                Text {
                    anchors.centerIn: parent
                    text: qsTr("SHUT DOWN")
                    color: "#e7d8dc"
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 13
                }
                MouseArea {
                    id: powerMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: if (sddm.canPowerOff) sddm.powerOff()
                }
            }
        }
    }

    Rectangle {
        id: sessionPopup
        visible: false
        z: 20
        x: panel.x + 46
        y: panel.y + 405
        width: (panel.width - 92) * 0.57
        height: Math.min(210, sessionList.contentHeight + 8)
        radius: 9
        color: "#f207131f"
        border.width: 1
        border.color: "#8ea9bd"

        ListView {
            id: sessionList
            anchors.fill: parent
            anchors.margins: 4
            clip: true
            model: sessionModel
            currentIndex: root.sessionIndex

            delegate: Rectangle {
                required property int index
                required property string name
                width: sessionList.width
                height: 42
                radius: 6
                color: index === root.sessionIndex ? "#587990" : (sessionItemMouse.containsMouse ? "#304e6375" : "transparent")

                Component.onCompleted: {
                    if (index === root.sessionIndex)
                        root.sessionName = name
                }
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: 12
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width - 24
                    text: name
                    color: "#ffffff"
                    elide: Text.ElideRight
                    font.family: config.stringValue("fontFamily")
                    font.pixelSize: 15
                }
                MouseArea {
                    id: sessionItemMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        root.sessionIndex = index
                        root.sessionName = name
                        sessionPopup.visible = false
                    }
                }
            }
        }
    }

    Text {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 54
        anchors.bottomMargin: 43
        text: Qt.formatDateTime(root.currentDate, "dddd, d MMMM  |  hh:mm:ss")
        color: "#d5e2eb"
        font.family: config.stringValue("fontFamily")
        font.pixelSize: 15
    }
}
