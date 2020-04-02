import React from 'react'
import PropTypes from 'prop-types'

import './stylesheets/StepSuccess.scss'
import Services from '@src/Services'


export default function StepSuccess(props){
  return (
    <div className='great-mvp-signup-wizard-step-success p-h-0' id="signup-modal-success">
      <h2 className="h-xl">Complete</h2>
      <p className='great-mvp-subtitle'>
        Your guidance on exporting {props.products.map((item, i) => <span key={i} className="great-mvp-pill-button">{item.label}</span>)} is ready
      </p>
      <form className="m-t-s" onSubmit={event => {event.preventDefault(); props.handleSubmit() }}>
        <input
          type="submit"
          value={Services.config.userIsAuthenticated ? 'Save your answers': "Sign up to save your answers" }
          id="signup-modal-submit-success"
          className="great-mvp-wizard-step-submit great-mvp-wizard-step-button"
          disabled={props.disabled}
        />
      </form>
    </div>
  )
}

StepSuccess.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  products: PropTypes.array.isRequired,
}
