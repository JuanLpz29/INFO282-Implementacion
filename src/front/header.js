class MainHeader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <header class="header">
                <div class="inner-header">
                    <div class="logo-container">
                        <h1><a href ="index.html" > La Tentación</a></h1>
                    </div>
                        <ul class="navigation">
                            <a href="index.html"><li>Inicio</li></a>
                            <a href="inventario.html"><li>Subir Compra</li></a>
                            <a href="productos.html"><li>Productos</li></a>
                            <a href=""><li>Usuarios</li></a>
                            <a href=""><li>Configuración</li></a>
                        </ul>
                </div>
        </header>
        
      `;
    }
}

customElements.define("main-header", MainHeader);
