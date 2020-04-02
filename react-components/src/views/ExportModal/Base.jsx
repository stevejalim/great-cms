import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import ReactModal from 'react-modal'

import Modal from '@src/components/Modal'
import Services from '@src/Services'
import Wizard, { STEP_CATEGORY, STEP_SUCCESS } from './Wizard'

import './stylesheets/Modal.scss'
//import '@src/stylesheets/Base.scss'



const LABEL_NO_SIGN_IN = 'Continue without signing in'
const LABEL_GENRIC_CONTENT =  'No thanks I would like generic content'

export function Base(props){

  const [modalIsOpen, setModalIsOpen] = React.useState(props.isOpen)
  const [currentStep, setCurrentStep] = React.useState(props.currentStep)
  const isLastStep = currentStep == STEP_SUCCESS

  function onComplete(products) {
    setModalIsOpen(false)
    props.onComplete(products)
  }

  function SkipShowGenericContent(props) {
    const children = []
    if (!Services.config.userIsAuthenticated) {
      children.push(
        <a
          href='#'
          className='great-mvp-wizard-step-link'
          onClick={event => { event.preventDefault(); props.onClick() }}
        >{isLastStep ? LABEL_NO_SIGN_IN : LABEL_GENRIC_CONTENT}</a>
      )
    }
    if (isLastStep) {
      children.push(
        <p className="m-t-xxs"><a
          href='#'
          className='great-mvp-wizard-step-link'
          onClick={event => { event.preventDefault(); setCurrentStep(STEP_CATEGORY) }}
        >Change answers</a></p>
      )
    }
    if (children.length > 0) {
      return (
        <div className="grid p-t-s">
          <div className="c-1-3">&nbsp;</div>
          <div className="c-2-3">{children}</div>
        </div>
      )
    }
    return null
  }

  return (
    <Modal
      isOpen={modalIsOpen}
      setIsOpen={setModalIsOpen}
      id='dashboard-question-modal-export'
      skipFeatureCookieName='skip-export'
      skipFeatureComponent={SkipShowGenericContent}
      className='ReactModal__Content--Export p-v-s p-r-s'
    >
      <div className="grid">
        <aside className="c-1-3">
          <img src='/static/images/book-chap.png' className="book-chap-image" />
        </aside>
        <div className="c-2-3">
          <Wizard
            currentStep={currentStep}
            setCurrentStep={setCurrentStep}
            onComplete={onComplete}
          />
        </div>
      </div>
    </Modal>
  )
}

Base.propTypes = {
  isOpen: PropTypes.bool,
  onComplete: PropTypes.func,
  currentStep: PropTypes.string,
}

Base.defaultProps = {
  isOpen: false,
  currentStep: STEP_CATEGORY,
  onComplete: () => {},
}


export default function createModal({ element, ...params }) {
  ReactModal.setAppElement(element)
  ReactDOM.render(<Base {...params} />, element)
}

