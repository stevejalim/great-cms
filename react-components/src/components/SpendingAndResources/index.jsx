import React, { useState } from 'react'
import PropTypes from 'prop-types'

import { TextArea } from '@src/components/Form/TextArea'
import Services from '../../Services'

import { analytics } from '@src/Helpers'

export const SpendingAndResources = ({
  field,
  formFields,
  formData,
}) => {

  const [input, setInput] = useState(formData)
  const [pushedAnalytic, setPushedAnalytic] = useState(false)


  const pushAnalytics = () => {
    // function to make sure we pushed analytics only once as per Andy Wong requirement
    // The way component build it trigger save on every key stroke which floods the analytics
    if (!pushedAnalytic) {
      analytics({
        'event': 'planSectionSaved',
        'sectionTitle': 'marketing-approach'
      })
      setPushedAnalytic(true)
    }
  }

  const update = (e) => {
    setInput({ ...e })
    Services.updateExportPlan({ [field]: { ...e }})
      .then(pushAnalytics)
      .catch(() => {})
  }

  return (
    <>
      {formFields.map(item => (
        <TextArea
          tooltip={item.tooltip}
          label={item.label}
          example={item.example}
          key={item.name}
          id={item.name}
          value={input[item.name]}
          description={item.description}
          placeholder={Number.isInteger(item.placeholder) ? item.placeholder : 'Add some text'}
          currency={item.currency}
          tag={Number.isInteger(item.placeholder) ? 'number' : 'text'}
          onChange={update}
        />
      ))}
    </>
  )
}

SpendingAndResources.propTypes = {
  field: PropTypes.string.isRequired,
  formData: PropTypes.objectOf(PropTypes.string).isRequired,
  formFields: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    placeholder: PropTypes.string.isRequired,
  })).isRequired,
}
