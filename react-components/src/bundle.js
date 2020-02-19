import '../../core/sass/base.scss'
import 'great-styles/src/great-styles.scss'

import SignupModal from '@src/views/SignupModal/Modal'
import QuestionModal from '@src/views/QuestionModal/Modal'

import {STEP_CREDENTIALS, STEP_VERIFICATION_CODE} from '@src/views/SignupModal/Wizard/'
import Services from '@src/Services'
import '@babel/polyfill'

export default {
  setConfig: Services.setConfig,
  SignupModal,
  QuestionModal,
  STEP_CREDENTIALS,
  STEP_VERIFICATION_CODE,
};
