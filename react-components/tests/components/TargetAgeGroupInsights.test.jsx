import React from 'react'
import { shallow } from 'enzyme'
import { TargetAgeGroupInsights } from '@src/components/TargetAgeGroupInsights/TargetAgeGroupInsights'

let wrapper
const mockGroups = [
  { key: '0_9', label: '0-9 year olds' },
  { key: '10_19', label: '10-19 year olds' },
  { key: '20_29', label: '20-29 year olds' },
  { key: '30_39', label: '30-39 year olds' }
]

describe('TargetAgeGroupInsights', () => {
  beforeEach(() => {
    wrapper = shallow(<TargetAgeGroupInsights groups={mockGroups} />)
  })

  afterEach(() => {
    wrapper = null
  })

  test('renders heading and select button initially', () => {
    expect(wrapper.find('.target-age-group-insights__heading').length).toEqual(1)
    expect(wrapper.find('.target-age-group-insights__select-button').length).toEqual(1)
    expect(wrapper.find('form').length).toEqual(0)
    expect(wrapper.find('Table').length).toEqual(0)
  })

  test('renders form', () => {
    expect(wrapper.instance().state.isOpen).toBe(false)
    wrapper.find('.target-age-group-insights__select-button').simulate('click', { type: 'click' })
    expect(wrapper.instance().state.isOpen).toBe(true)
    expect(wrapper.find('form').length).toEqual(1)
    expect(wrapper.find('Table').length).toEqual(0)
  })

  test('renders table', () => {
    wrapper.find('.target-age-group-insights__select-button').simulate('click', { type: 'click' })
    wrapper
      .find('form input')
      .first()
      .simulate('change', { type: 'change', target: { value: mockGroups[0]['key'] } })

    wrapper.find('form').simulate('submit', { preventDefault: () => {} })
    expect(wrapper.instance().state.isOpen).toBe(false)
    expect(wrapper.find('form').length).toEqual(0)
    expect(wrapper.find('Table').length).toEqual(1)
  })
})
