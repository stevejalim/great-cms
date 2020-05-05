import { decorate } from '@storybook/addon-actions'
import { withKnobs, select } from '@storybook/addon-knobs'
import iconDocs from './icon.mdx'
import './icon.js'

const decoratedAction = decorate([() => ['Click']])

export default {
  title: 'Icon',
  parameters: {
    docs: { page: iconDocs },
    decorators: [withKnobs],
    'in-dsm': {
      docFilePath: './icon.docs.json',
      containerClass: 'sample-code',
      id: '<DSM component container ID>',
    },
  },
}

const availableIcons = {
  dots: 'dots',
  menu: 'menu',
  play: 'play',
  plus: 'plus',
}
const availableSizes = {
  sm: 'sm',
  lg: 'lg',
  xl: 'xl',
  xxl: 'xxl',
}

export const All = () => {
  const size = select('size', availableSizes, availableSizes.lg)
  return decoratedAction.withActions({ 'click great-icon': 'Great icon clicked' })(
    () =>
      `<div class="sample-code" size="lg">
        ${Object.values(availableIcons)
          .map((name) => `<great-icon name="${name}" size="${size}"></great-icon>`)
          .join('&emsp;&emsp;&emsp;')}
      </div>`
  )
}

export const Single = () => {
  const name = select('name', availableIcons, availableIcons.dots)
  const size = select('size', availableSizes, availableSizes.lg)
  return decoratedAction.withActions({ 'click great-icon': 'Great icon clicked' })(
    () =>
      `<div class="sample-code">
          <great-icon name="${name}" size="${size}"></great-icon>
      </div>`
  )
}
