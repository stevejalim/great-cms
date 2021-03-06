import React, { useState } from 'react'
import PropTypes from 'prop-types'
import ReactModal from 'react-modal'

import { Modal } from '@src/components/Modal/index'
import { CountryFinderModal } from '../../ProductFinder/CountryFinder'

export const CountryNotSelected = ({ isOpen }) => {

  const [modal, setModal] = useState(isOpen)
  const [modalIsOpen, setIsOpen] = useState(false)

  const openCountryFinder = () => {
    setIsOpen(true)
    setModal(false)
  }

  return (
    <>
      <ReactModal
        isOpen={modal}
        className='ReactModal__Content ReactModalCentreScreen'
        overlayClassName='ReactModal__Overlay ReactModalCentreScreen'
        contentLabel='Modal'
      >
        <Modal
          backUrl='/export-plan/dashboard/'
          header='Add your target market'
          content='You will need to choose a target market before you can complete this section'
          onClick={openCountryFinder}
          buttonText='Add a target market'
          type={1}
        />
      </ReactModal>
      <CountryFinderModal
        modalIsOpen={modalIsOpen}
        setIsOpen={setIsOpen}
        addButton={false}
      />
    </>
  )
}

CountryNotSelected.propTypes = {
  isOpen: PropTypes.bool.isRequired,
}
