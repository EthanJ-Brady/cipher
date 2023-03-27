class Menu {
    constructor() {
        this.element = document.getElementById("menu");
        
        this.mask = stringToHtml('<div class="menu__mask"></div>');
        this.mask.onclick = () => this.hide();

        this.close = this.element.querySelector(".menu__close");
        this.close.onclick = () => this.hide();
    }
    
    show() {
        this.element.classList.add("menu--shown");
        this.element.appendChild(this.mask);
    }

    hide() {
        this.element.classList.remove("menu--shown");
        this.mask.remove();
    }
}