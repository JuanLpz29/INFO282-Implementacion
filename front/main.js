const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow(production) {
    const win = new BrowserWindow({
        autoHideMenuBar: true,
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            webSecurity: true,
        },
    });

    win.loadFile("dist/index.html");
    if (production) {
        win.webPreferences['devTools'] = false
    }
    else {
        win.webContents.openDevTools()
    }
}

app.whenReady().then(() => {
    createWindow(app.isPackaged);

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
