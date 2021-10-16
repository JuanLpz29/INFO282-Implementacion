class  MainHeader extends HTMLElement{
    connectedCallback() {
        this.innerHTML = `
            <header class="header">
                <div class="inner-header">
                    <div class="logo-container">
                        <h1>La Tentación</h1>
                    </div>
                        <ul class="navigation">
                            <a href=""><li>Inicio</li></a>
                            <a href=""><li>Inventario</li></a>
                            <a href=""><li>Ventas</li></a>
                            <a href=""><li>Usuarios</li></a>
                            <a href=""><li>Configuración</li></a>
                        </ul>
                </div>
        </header>
        
      `  
    }
}

customElements.define('main-header', MainHeader)