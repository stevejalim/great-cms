import React from 'react'
import Modal from 'react-modal'

import { act } from 'react-dom/test-utils'
import { mount, shallow } from 'enzyme'
import Enzyme from 'enzyme'
import Adapter from 'enzyme-adapter-react-16'

import { LoginModal } from '../src/LoginModal'
import ErrorList from '../src/ErrorList'

import Services from '../src/Services'


Enzyme.configure({ adapter: new Adapter() })

jest.mock('../src/Services');

const formUrl = 'http://www.example.com'
const csrfToken = '123'
const createEvent = () => ({ preventDefault: jest.fn() })


beforeEach(() => {
  jest.useFakeTimers()
})

afterEach(() => {
  jest.useRealTimers()
})

test('Modal opens and closes on link click', () => {
  const component = shallow(<LoginModal loginUrl={formUrl} csrfToken={csrfToken} />)
  const event = createEvent()

  // when the user clicks the button
  act(() => {
    component.find('#header-sign-in-link').simulate('click', event)
  })

  // then the modal s open
  expect(component.find(Modal).prop('isOpen')).toEqual(true)
  expect(event.preventDefault).toBeCalled()

  // when the user clicks the close button
  act(() => {
    component.find(Modal).find(".link").simulate('click', event)
  })

  // then the modal is closed
  expect(component.find(Modal).prop('isOpen')).toEqual(false)

})

test('Modal shows error message', () => {
  // when there is an error
  const component = shallow(
    <LoginModal loginUrl={formUrl} csrfToken={csrfToken} isOpen={true} errorMessage={'some error'} />
  )
  // then the validation message is displayed
  expect(component.find(ErrorList).prop('message')).toEqual('some error')
})

test('Modal form elements are disabled while in progress', () => {
  // when the form submission is in progress
  const component = mount(<LoginModal loginUrl={formUrl} csrfToken={csrfToken} isOpen={true} isInProgress={true} />)
  // then the form elements are disabled
  expect(component.find('input[name="username"]').getDOMNode().disabled).toEqual(true)
  expect(component.find('input[name="password"]').getDOMNode().disabled).toEqual(true)
  expect(component.find('input[type="submit"]').getDOMNode().disabled).toEqual(true)

})

test('Modal form elements are not disabled while not in progress', () => {
  // when the form submission is in progress
  const component = mount(<LoginModal loginUrl={formUrl} csrfToken={csrfToken} isOpen={true} isInProgress={false} />)
  // then the form elements are disabled
  expect(component.find('input[name="username"]').getDOMNode().disabled).toEqual(false)
  expect(component.find('input[name="password"]').getDOMNode().disabled).toEqual(false)
  expect(component.find('input[type="submit"]').getDOMNode().disabled).toEqual(false)
})


describe('Modal end to end', () => {

  const { reload } = window.location

  beforeEach(() => {
    delete window.location
    window.location = { reload: jest.fn() }
  })

  afterEach(() => {
    window.location.reload = reload
  })

  test('bad credentials results in error message', done => {
    // given the credentials are incorrect
    const event = createEvent()
    Services.checkCredentials.mockImplementation(() => Promise.reject('An erorr occured'));

    const component = mount(<LoginModal loginUrl={formUrl} csrfToken={csrfToken} isOpen={true} />)

    act(() => {
      component.find('input[name="username"]').getDOMNode().value = 'username'
      component.find('input[name="password"]').getDOMNode().value = 'password'
      component.find('form').simulate('submit', event)
    })

    // then an error message is displayed
    setImmediate(() => {
      component.update()
      expect(component.find(ErrorList).prop('message')).toEqual('An erorr occured')
      expect(window.location.reload).not.toHaveBeenCalled()
      done()
    })
  })

  test('good credentials results in page reload', done => {
    // given the credentials are correct
    const event = createEvent()
    Services.checkCredentials.mockImplementation(() => Promise.resolve());

    const component = mount(<LoginModal loginUrl={formUrl} csrfToken={csrfToken} isOpen={true} />)

    act(() => {
      component.find('input[name="username"]').getDOMNode().value = 'username'
      component.find('input[name="password"]').getDOMNode().value = 'password'
      component.find('form').simulate('submit', event)
    })

    // then an error message is not displayed
    setImmediate(() => {
      expect(component.find(ErrorList).length).toEqual(0)
      expect(window.location.reload).toHaveBeenCalled()
      done()
    })

  })

})
