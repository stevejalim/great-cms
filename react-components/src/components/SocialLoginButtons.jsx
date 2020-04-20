/* eslint-disable */
import React from 'react'

import googleIcon from '@assets/google-icon.png'
import linkedinIcon from '@assets/linkedin-icon.png'
import Services from '../Services'

import './stylesheets/SocialLoginButtons.scss'


export default function SocialLoginButtons(props){
  return (
    <div className="great-mvp-social-login-buttons">
      <a href={Services.config.linkedInUrl} id="signup-modal-linkedin" className="great-mvp-wizard-step-button m-t-0 m-b-xs">
        <img src={linkedinIcon} />
        <span>Continue with LinkedIn</span>
      </a>
      <a href={Services.config.googleUrl} id="signup-modal-google" className="great-mvp-wizard-step-button m-t-0 m-b-xs">
        <img src={googleIcon} />
        <span>Continue with Google</span>
      </a>
    </div>
  )
}
