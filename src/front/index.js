const { app, BrowserWindow, Menu } = require('electron');
const url = require('url');
const path = require('path');

if (process.env.NODE_ENV !== 'production') {
    require('electron-reload')(__dirname, {
        electron: path.join(__dirname, '../../node_modules', '.bin', 'electron',)
    });

}

let mainWindow

function createWindow() {

    console.log("app is ready")
    mainWindow = new BrowserWindow({});
    mainWindow.maximize()

    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'views/index.html'),
        protocol: 'file',
        slashes: true
    }));

    mainWindow.on('closed', () => {
        app.quit();
    })

    const mainMenu = Menu.buildFromTemplate(templateMenu);
    Menu.setApplicationMenu(mainMenu)

}

app.on('ready', createWindow)

app.on('activate', function () {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) {
        createWindow()
    }
})

const templateMenu = [
    {
        label: 'File',
        submenu: [
            {
                label: 'New Product',
                acceleratior: 'Ctrl+N',
                click() {
                    createNewProduct()
                }
            }
        ]
    },
    {
        label: 'Test',
        submenu: [
            {
                label: 'Test submenu'
            }
        ]
    },
    {
        label: 'Exit',
        submenu: [
            {
                label: 'Exit',
                acceleratior: 'Ctrl+Q',
                click() {
                    app.quit();
                }
            }
        ]
    }
]

if (process.env.NODE_ENV !== 'production') {
    templateMenu.push({
        label: 'DevTools',
        submenu: [{
            label: 'Show, Hide',
            click(item, focusedWindow) {
                focusedWindow.toggleDevTools();
            },
        }]


    })
}




