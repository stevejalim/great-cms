import React from 'react'
import PropTypes from 'prop-types'
import EducationalMomentTooltip from '../../EducationalMomentTooltip'
import ErrorList from '../../ErrorList'

export const FormGroup = ({
  children,
  errors,
  tooltip,
  id,
  label,
  description,
  example,
  hideLabel
}) => (
  <div
    className={`form-group ${errors.length > 0 ? 'form-group-error' : ''}`}
  >
    {
      tooltip &&
      <EducationalMomentTooltip
        heading=''
        description={tooltip}
        id={id}
        type='LEFT'
      />
    }
    <label className={`form-label ${hideLabel ? 'visually-hidden': ''}`} htmlFor={id}>{label}</label>
    { description && <div className='text-blue-deep-80 p-t-xs p-b-xxs' dangerouslySetInnerHTML={{ __html: description }} /> }
    {
      example &&
      <dl className='form-group-example bg-blue-deep-10 p-xs m-b-xs'>
        <dt className='body-l-b'>A fictional example to help you complete this section</dt>
        <dd className='m-t-xxs body-l' dangerouslySetInnerHTML={{ __html: example }} />
      </dl>
    }
    <ErrorList
      errors={errors}
    />
    {children}
  </div>
)

FormGroup.propTypes = {
  children: PropTypes.element.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string),
  tooltip: PropTypes.string,
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  description: PropTypes.string,
  example: PropTypes.string,
  hideLabel: PropTypes.bool,
}

FormGroup.defaultProps = {
  errors: [],
  description: '',
  tooltip: '',
  example: '',
  hideLabel: false
}
