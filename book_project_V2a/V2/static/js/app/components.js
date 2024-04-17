class MyPicker extends HTMLElement {
    constructor() {
        super();
	}
	
	connectedCallback() {

		var _id = this.getAttribute("id")
		console.log(this.getAttribute("x-name"));
		//console.log(this.innerHTML);

		var newDiv = '<div>'
		newDiv += '<input type="hidden" id="val_' + _id + '" name="model_id"></input>'
		newDiv += '<input type="hidden" id="txt_' + _id + '" name="model_name"></input>'
		//newDiv += this.innerHTML 
		//newDiv += 'Welcome to MyPIcker'
		newDiv += '<select class="form-select form-select-sm mx-2" style="min-width:150px;">'
		newDiv += this.innerHTML
		newDiv += '</select>'
		newDiv += '</div>'

		this.innerHTML = newDiv;
		//console.log(this.innerHTML);

        // Create a shadow DOM for encapsulation
        //this.attachShadow({ mode: 'open' });
        //const inp = document.createElement('input');
        // Append the select to the shadow DOM
        //this.shadowRoot.appendChild(inp);

		//const shadowRoot = this.attachShadow({ mode: 'closed' });
        //const inp = document.createElement('input');
		//shadowRoot.appendChild(newDiv);
    }
}

// Define the custom element
customElements.define('my-picker', MyPicker);

class ColorPicker extends HTMLElement {
    constructor() {
        super();
        // Create a shadow DOM for encapsulation
        this.attachShadow({ mode: 'open' });

        // Define the list of colors
        this.colors = ['red', 'green', 'blue', 'yellow'];

        // Create a select element
        const select = document.createElement('select');
        select.id = 'colorSelect';
		//select.setAttribute("class", "form-select form-select-sm mx-2");
		//select.class = 'form-select form-select-sm mx-2'
		//select.className = 'form-select form-select-sm mx-2'
		select.className = this.className

        // Populate the select with color options
        this.colors.forEach(color => {
            const option = document.createElement('option');
            option.value = color;
            option.textContent = color;
            select.appendChild(option);
        });

        // Add event listener for selection change
        select.addEventListener('change', () => {
            this.dispatchEvent(new CustomEvent('colorSelected', {
                detail: { selectedColor: select.value },
                bubbles: true,
                composed: true
            }));
        });

        // Append the select to the shadow DOM
        this.shadowRoot.appendChild(select);
    }
}

// Define the custom element
customElements.define('color-picker', ColorPicker);

class MyComponent extends HTMLElement {
  connectedCallback() {	  
  console.log(this.getAttribute("class"));
  this.innerHTML = `<div class='bg-primary'>` + this.innerHTML + `</div>`
  console.log(this.innerHTML);
}

  disconnectedCallback() {
      console.log("I am leaving");
  }
}

customElements.define('my-component', MyComponent);

/*
class MyTable extends HTMLElement {
	constructor() {
        super();
	
	if (this.hasAttribute('src')) this.src = this.getAttribute('src');
    // If no source, do nothing
    if(!this.src) return;
		
	// attributes to do, datakey + cols
    if(this.hasAttribute('cols')) this.cols = this.getAttribute('cols').split(',');


    const shadow = this.attachShadow({
        mode: 'open'
    });
	
	const wrapper = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');
    wrapper.append(thead, tbody);
    shadow.appendChild(wrapper);	
	}
	async load() {
        console.log('load', this.src);
        // error handling needs to be done :|
        let result = await fetch(this.src);
        this.data = await result.json();
        this.render();
    }

    render() {
        console.log('render time', this.data);
        if(!this.cols) this.cols = Object.keys(this.data[0]);

        this.renderHeader();
        this.renderBody();
    }

    renderBody() {

        let result = '';
        this.data.books.forEach(c => {
            let r = '<tr>';
            this.cols.forEach(col => {
                r += `<td>${c[col]}</td>`;
            });
            r += '</tr>';
            result += r;
        });

        let tbody = this.shadowRoot.querySelector('tbody');
        tbody.innerHTML = result;

    }

    renderHeader() {

        let header = '<tr>';
        this.cols.forEach(col => {
            header += `<th>${col}</th>`;
        });
        let thead = this.shadowRoot.querySelector('thead');
        thead.innerHTML = header;

    }

    static get observedAttributes() { return ['src']; }

    attributeChangedCallback(name, oldValue, newValue) {
        // even though we only listen to src, be sure
        if(name === 'src') {
            this.src = newValue;
            this.load();
        }
    }	
}


customElements.define('my-table', MyTable);
*/

