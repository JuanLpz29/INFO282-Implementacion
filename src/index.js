const { app, BrowserWindow, Menu } = require('electron');
const url = require('url');
const path = require('path');

if (process.env.NODE_ENV !== 'production') {
    require('electron-reload')(__dirname, {})
    require('electron-reload')(__dirname, {
        electron: path.join(__dirname, '../node_modules', '.bin', 'electron')
    });
}

let mainWindow
let newProductWindow

app.on('ready', () => {
    mainWindow = new BrowserWindow({});

    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'views/index.html'),
        protocol: 'file',
        slashes: true
    }));

    const mainMenu = Menu.buildFromTemplate(templateMenu);
    Menu.setApplicationMenu(mainMenu)

    mainWindow.on('closed', () => {
        app.quit();
    })

});


function createNewProduct(){
    newProductWindow = new BrowserWindow({
        width: 400,
        height: 400,
        title: "New product"

    });
    newProductWindow.setMenu(null)
    newProductWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'views/second-window.html'),
        protocol: 'file',
        slashes: true
    }));

    newProductWindow.on('closed', () => {
        newProductWindow = null;
    })
}



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
        label:'Exit',
        submenu: [
            {
                label: 'Exit',
                acceleratior:'Ctrl+Q',
                click(){
                    app.quit();
                }
            }
        ]
    }
]

if (process.env.NODE_ENV !== 'production') {
    templateMenu.push({
        label:'DevTools',
        submenu: [{
            label:'Show, Hide',
            click(item, focusedWindow){
                focusedWindow.toggleDevTools();
            },
        }]

        
    })
}




