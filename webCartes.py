import sys
from PyQt5.QtCore import QUrl, Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,  QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QDesktopServices


class BrowserView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._temp_views = []  # Empêche la collecte prématurée des vues temporaires

    def createWindow(self, _type):
        # Intercepte window.open(...) pour ouvrir dans le navigateur par défaut
        temp_view = QWebEngineView(self)
        self._temp_views.append(temp_view)

        def _on_url_changed(url):
            QDesktopServices.openUrl(url)
            try:
                self._temp_views.remove(temp_view)
            except ValueError:
                pass
            temp_view.deleteLater()

        temp_view.urlChanged.connect(_on_url_changed)
        return temp_view


class Navigateur(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HAUHINE - CARTES MARINES")
        self.setGeometry(200, 100, 1200, 800)

        self.setWindowIcon(QIcon("./VoilierImage.ico"))

        # Vue Web
        self.browser = BrowserView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/"))
        self.setCentralWidget(self.browser)

        # Intercepter les touches directement au niveau de la WebView
        self.browser.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.browser and event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_F1:
                event.accept()
                QDesktopServices.openUrl(QUrl("http://127.0.0.1:5001/cartes"))
                return True
            elif key == Qt.Key_F2:
                event.accept()
                QDesktopServices.openUrl(QUrl("http://127.0.0.1:5000/?lancerHistorique=true&idCarte=123"))
                return True
            elif key == Qt.Key_F3:
                event.accept()
                profile = self.browser.page().profile()

                profile.clearHttpCache()  # Cache HTTP
                profile.clearAllPersistentData()  # LocalStorage, IndexedDB, etc.
                profile.clearAllVisitedLinks()  # Historique
                profile.cookieStore().deleteAllCookies()  # Cookies

                print("Cache et données effacés — JS/CSS seront rechargés.")
                return True

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter l'application ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        # Fallback (si jamais l'eventFilter ne capte pas l'événement)
        if event.key() == Qt.Key_F1:
            event.accept()
            QDesktopServices.openUrl(QUrl("http://127.0.0.1:5001/cartes"))
            return
        if event.key() == Qt.Key_F2:
            event.accept()
            QDesktopServices.openUrl(QUrl("http://127.0.0.1:5000/?lancerHistorique=true&idCarte=123"))
            return
        elif event.key() == Qt.Key_F3:
            event.accept()
            profile = self.browser.page().profile()

            profile.clearHttpCache()  # Cache HTTP
            profile.clearAllPersistentData()  # LocalStorage, IndexedDB, etc.
            profile.clearAllVisitedLinks()  # Historique
            profile.cookieStore().deleteAllCookies()  # Cookies
            print("Cache et données effacés — JS/CSS seront rechargés.")
            return True

        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Navigateur()
    window.show()
    sys.exit(app.exec_())
