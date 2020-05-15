import '../spinner/spinner'
import '../icon/icon'
import convertAttributesToObject from '../../utils/convertAttributesToObject'
import template from './button.html'
import styles from './button.css'

customElements.define(
    'great-button',
    class extends HTMLElement {
        // Attributes that when changed will trigger 'attributeChangedCallback' method
        static get observedAttributes() {
            return ['disabled', 'icon', 'loading', 'theme']
        }

        constructor() {
            super()

            // Create the shadowRoot that would contain our encapsulated component like an iframe
            this.shadow = this.attachShadow({ mode: 'open' })

            // template is just text equivalent to button.html, we need to create a DOM and render it first
            const { content } = new DOMParser().parseFromString(template, 'text/html').querySelector('template')
            this.shadow.appendChild(content.cloneNode(true))

            // styles that are imported from 'button.css' should also be attached to the shadowRoot
            // these will encapsulate the web component appearance, no styles on the parent document will apply
            const stylesheet = document.createElement('style')
            stylesheet.innerHTML = styles
            this.shadow.appendChild(stylesheet)

            // Select the button element that came from our template and manipulate its attributes
            this.button = this.shadow.querySelector('button')

            this.buttonContent = this.shadow.querySelector('.content')

            // Gets the text passed to the host component and renders it into our content span
            // e.g. <great-button>Render this text</great-button> will render "Render this text"
        }

        // Use 'attributeChangedCallback' lifecycle method to allow this component react on attr changes in a dynamic way
        // If we are to set these in the constructor any attr that changes past component initialisation won't trigger this code
        // attributes on the host element e.g. <great-button> are not guarantied to be present in the constructor
        attributeChangedCallback(name, oldValue, newValue) {
            const { disabled, theme } = convertAttributesToObject({ self: this })
            const availableThemes = ['primary', 'secondary', 'tertiary']

            switch (name) {
                case 'icon':
                    if (newValue !== undefined) {
                        const iconTheme = ['primary', 'secondary'].includes(theme) ? 'secondary' : 'primary'
                        const greatIcon = document.createElement('great-icon')
                        if (disabled !== undefined) greatIcon.setAttribute('disabled', disabled)
                        greatIcon.setAttribute('name', newValue)
                        greatIcon.setAttribute('theme', iconTheme)
                        greatIcon.setAttribute('size', 'sm')
                        this.button.prepend(greatIcon)
                    }
                    break
                case 'loading':
                    if (newValue !== undefined) {
                        const greatSpinner = document.createElement('great-spinner')
                        greatSpinner.setAttribute('size', 'sm')
                        greatSpinner.setAttribute('theme', theme === 'tertiary' ? 'dark' : 'light')
                        this.button.classList.add('loading')
                        this.button.prepend(greatSpinner)
                    }
                    break
                case 'theme':
                    if (availableThemes.includes(newValue)) {
                        if (oldValue) this.button.classList.remove(oldValue)
                        this.button.classList.add(newValue)
                    }
                    break
                default:
            }
        }

        // A lifecycle method that fires when the element is attached to the DOM, we are guaranteed to have
        // access to other custom elements on the DOM and also to get host attributes
        connectedCallback() {
            // Gets all attributes passed to the root custom component
            // filters attrs that are already used or like 'class' and 'style' enforcing style encapsulation
            const { class: className, icon, loading, style, theme, ...rest } = convertAttributesToObject({ self: this })

            // Passes down all attributes from to the parent component like type="submit", aria-hidden="true", data-test="great-button"
            Object.entries(rest).forEach(([key, value]) => this.button.setAttribute(key, value))

            this.buttonContent.innerHTML = this.textContent
        }
    }
)
