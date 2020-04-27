import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import ReactModal from 'react-modal'
import { connect, Provider } from 'react-redux'

import Component, { STEP_CATEGORY, STEP_PRODUCTS, STEP_SUCCESS } from '@src/views/ProductsModal/Component'
import Services from '@src/Services'
import actions from '@src/actions'
import { getModalIsOpen, getPerformFeatureSKipCookieCheck, getProductsExpertise } from '@src/reducers'


export function Container(props){
  const [errors, setErrors] = React.useState(props.errors)
  const [category, setCategory] = React.useState(props.category)
  const [isInProgress, setIsInProgress] = React.useState(props.isInProgress)
  const [currentStep, setCurrentStep] = React.useState(props.currentStep)

  function handleCategoryChange(value) {
    setCategory(value)
    setIsInProgress(false)
    setErrors({})
    setCurrentStep(STEP_PRODUCTS)
  }

  function handleProductsSubmit() {
    setIsInProgress(false)
    setErrors({})
    setCategory('')  // so if the user goes back to step 1 they have to click again
    setCurrentStep(STEP_SUCCESS)
  }

  function handleChangeAnswers() {
    setCurrentStep(STEP_CATEGORY)
  }

  function handleSignup() {
    props.setIsSignupModalOpen(true) 
  }

  function handleComplete() {
    const reducer = (accumulator, product) => `${accumulator}product_code=${product.value}&product=${product.label}&`
    const url = props.products.reduce(reducer, location.pathname + '?')
    window.location.assign(url)
  }

  return (
    <Component
      errors={errors}
      category={category}
      isInProgress={isInProgress}
      currentStep={currentStep}
      handleSignup={handleSignup}
      handleComplete={handleComplete}
      handleCategoryChange={handleCategoryChange}
      handleProductsSubmit={handleProductsSubmit}
      handleChangeAnswers={handleChangeAnswers}
      {...props}
    />
  )
}


const mapStateToProps = state => {
  return {
    isOpen: getModalIsOpen(state, 'products'),
    products: getProductsExpertise(state),
    performSkipFeatureCookieCheck: getPerformFeatureSKipCookieCheck(state),
  }
}

const mapDispatchToProps = dispatch => {
  return {
    setIsOpen: isOpen => { dispatch(actions.toggleModalIsOpen('products', isOpen))},
    setIsSignupModalOpen: isOpen => { dispatch(actions.toggleModalIsOpen('signup', isOpen))},
    setProducts: products => { dispatch(actions.setProductsExpertise(products)) },
  }
}

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container)

export default function({ element, ...params }) {
  ReactModal.setAppElement(element)
  ReactDOM.render(
    <Provider store={Services.store}>
      <ConnectedContainer {...params} />
    </Provider>,
    element
  )
}