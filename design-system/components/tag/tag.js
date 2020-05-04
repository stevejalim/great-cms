import template from './tag.html'
import styles from './tag.scss'

customElements.define(
  'great-tag',
  class extends HTMLElement {
    constructor() {
      super()
        
      const stylesheet = document.createElement('style')
      stylesheet.innerHTML = styles

      const attributes = this.getAttributeNames().reduce((accumulator, attribute) => {
        accumulator[attribute] = this.getAttribute(attribute)
        return accumulator
      }, {})

      const { class: className, disabled, icon, loading, style, theme, ...rest } = attributes

      const shadowRoot = this.attachShadow({ mode: 'open' })
      shadowRoot.innerHTML = template
      shadowRoot.appendChild(stylesheet)

      const tag = shadowRoot.querySelector('button')
      tag.classList.add(theme);

      if (disabled || disabled === '') tag.setAttribute('disabled', '')
      Object.entries(rest).forEach(([key, value]) => tag.setAttribute(key, value))

      tag.textContent = this.textContent
    }
  }
)
