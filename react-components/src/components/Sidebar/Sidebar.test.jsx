import React from  'react'
import { render, fireEvent, waitFor } from '@testing-library/react'

import { Sidebar } from '.'

const props = {
  logo: 'www.example.com/image.jpg',
  company: 'Nike',
  sections: [
    { title: 'about us', url: 'section/about-us'},
    { title: 'contact us', url: 'section/contact-us'},
    { title: 'our blog', url: 'section/our-blog'},
  ]
}

const setup = ({...data}) => {

  const utils = render(<Sidebar {...data} />)

  return {
    ...utils
  }
}

describe('Sidebar', () => {
  describe('Should be collapsed', () => {
    const { container, getAllByRole } = setup(props)
    const nav = container.firstChild
    const buttons = getAllByRole('button')
    const icon = buttons[0].firstChild

    it('Should have close class', () => {
      expect(nav).toHaveClass('sidebar__close')
    })

    it('Should have expand icon', () => {
      expect(icon).toHaveClass('fa-angle-double-right')
    })
  })

  describe( 'logo', () => {
    it('Should company logo', () => {
      const { getByAltText } = setup(props)
      const image = getByAltText('Nike')
      expect(image).toBeInTheDocument()
    })

    it('Should display placeholder image', () => {
      const { getByAltText } = setup({...props, logo: '', company: ''})
      const image = getByAltText('Add a business logo')
      expect(image).toBeInTheDocument()
    })
  })

  describe('sections', () => {
    it('Should list sections', () => {
      const { getByTitle } = setup(props)
      expect(getByTitle('about us')).toBeInTheDocument()
      expect(getByTitle('contact us')).toBeInTheDocument()
      expect(getByTitle('our blog')).toBeInTheDocument()
    })
  })

  describe('Should be expanded', () => {
    it('Should be not have close class and have expanded icon',  async () => {
      const { container, getAllByRole } = setup(props)
      const nav = container.firstChild
      const buttons = getAllByRole('button')
      const toggleButton = buttons[0]
      const icon = buttons[0].firstChild
      fireEvent.click(toggleButton)

      await waitFor(() => {
        expect(nav).not.toHaveClass('sidebar__close')
        expect(icon).toHaveClass('fa-angle-double-left')
      })
    })
  })
})