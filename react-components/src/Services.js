const MESSAGE_UNEXPECTED_ERROR = {'__all__': ['Unexpected error']}
const MESSAGE_PERMISSION_DENIED = {'__all__': ['You do not have permission to perform this action']}
const MESSAGE_NOT_FOUND_ERROR = {'__all__': ['Not found']}
const MESSAGE_TIMEOUT_ERROR = {'__all__': ['Request timed out']}
const MESSAGE_BAD_REQUEST_ERROR = {'__all__': ['Bad request']}


const post = function(url, data) {
  return fetch(url, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': config.csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: JSON.stringify(data),
  })
}

const getCountryData = function(country) {
  return get(`${config.countryDataUrl}?country=${encodeURIComponent(country)}`).then(responseHandler)
}

const get = function(url, params) {
  const parsedUrl = new URL(`${location.origin}${url}`)
  const parsedParams = new URLSearchParams(params).toString();
  parsedUrl.search = parsedParams

  return fetch(parsedUrl, {
    method: 'get',
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': config.csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
}

const lookupProduct = function({q}) {
  return get(config.apiLookupProductUrl, {q}).then(response => responseHandler(response).json())
}


const createUser = function({email, password}) {
  return post(config.apiSignupUrl, {email, password}).then(responseHandler)
}


const checkVerificationCode = function({ email, code}) {
  return post(config.verifyCodeUrl, {email, code}).then(responseHandler)
}


const checkCredentials = function({ email, password }) {
  return post(config.apiLoginUrl, {email, password}).then(responseHandler)
}


const updateCompany = function({ expertise_industries, expertise_countries, expertise_products_services }) {
  const data = { expertise_industries, expertise_countries, expertise_products_services }
  return post(config.apiUpdateCompanyUrl, data).then(responseHandler)
}

const responseHandler = function(response) {
  if (response.status == 400) {
    return response.json().then(error => { throw error })
  } else if (response.status == 403) {
    throw MESSAGE_PERMISSION_DENIED
  } else if (response.status == 404) {
    throw MESSAGE_NOT_FOUND_ERROR
  } else if (response.status == 504) {
    throw MESSAGE_TIMEOUT_ERROR
  } else if (response.status == 400) {
    throw MESSAGE_BAD_REQUEST_ERROR
  } else if (response.status != 200) {
    throw MESSAGE_UNEXPECTED_ERROR
  } else if (response.status == 200) {
    return response.json()
  } else {
    return response
  }
}

// static values that will not change during execution of the code
let config = {}
const setConfig = function({
  countryDataUrl,
  apiLoginUrl,
  apiSignupUrl,
  apiLookupProductUrl,
  apiUpdateCompanyUrl,
  countryOptions,
  csrfToken,
  dashboardUrl,
  googleUrl,
  industryOptions,
  linkedInUrl,
  loginUrl,
  passwordResetUrl,
  termsUrl,
  userCountries,
  userIndustries,
  verifyCodeUrl,
  userIsAuthenticated,
}) {
  config.countryDataUrl = countryDataUrl
  config.apiLoginUrl = apiLoginUrl
  config.apiSignupUrl = apiSignupUrl
  config.apiLookupProductUrl = apiLookupProductUrl
  config.apiUpdateCompanyUrl = apiUpdateCompanyUrl
  config.countryOptions = countryOptions
  config.csrfToken = csrfToken
  config.dashboardUrl = dashboardUrl
  config.googleUrl = googleUrl
  config.industryOptions = industryOptions
  config.linkedInUrl = linkedInUrl
  config.loginUrl = loginUrl
  config.passwordResetUrl = passwordResetUrl
  config.termsUrl = termsUrl
  config.verifyCodeUrl = verifyCodeUrl
  config.userCountries = userCountries
  config.userIndustries = userIndustries
  config.userIsAuthenticated = userIsAuthenticated
}

export default {
  createUser,
  checkCredentials,
  checkVerificationCode,
  updateCompany,
  getCountryData,
  lookupProduct,
  setConfig,
  config,
  messages: {
    MESSAGE_UNEXPECTED_ERROR,
    MESSAGE_PERMISSION_DENIED,
    MESSAGE_NOT_FOUND_ERROR,
    MESSAGE_TIMEOUT_ERROR,
  }
}
