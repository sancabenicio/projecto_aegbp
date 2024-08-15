import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Spinner, Alert, Button, Form, Modal } from 'react-bootstrap';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import Header from './Header';
import Footer from './Footer';

const Voluntariado = () => {
  const { t } = useTranslation();
  const [oportunidades, setOportunidades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const [formData, setFormData] = useState({ name: '', email: '' });
  const [formError, setFormError] = useState(null);
  const [registrationSuccess, setRegistrationSuccess] = useState(null);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/volunteer-opportunities/`;

    axios.get(apiUrl)
      .then(response => {
        setOportunidades(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(t('voluntariado.errorLoadingOpportunities'));
        setLoading(false);
      });
  }, [t]);

  const validateForm = () => {
    const { name, email } = formData;

    if (!name || name.length < 2) {
      setFormError(t('voluntariado.invalidName'));
      return false;
    }

    if (!email || !validateEmail(email)) {
      setFormError(t('voluntariado.invalidEmail'));
      return false;
    }

    setFormError(null);
    return true;
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleRegister = (opportunityId) => {
    if (!validateForm()) {
      return;
    }

    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/volunteers/?opportunity=${opportunityId}`;

    axios.get(apiUrl)
      .then(response => {
        const registeredEmails = response.data.map(volunteer => volunteer.email);

        if (registeredEmails.includes(formData.email)) {
          setFormError(t('voluntariado.emailAlreadyRegistered'));
        } else {
          const registrationData = {
            opportunity: opportunityId,
            name: formData.name,
            email: formData.email,
          };

          axios.post(apiUrl, registrationData)
            .then(response => {
              setRegistrationSuccess(t('voluntariado.successMessage', { title: selectedOpportunity.title }));
              setFormData({ name: '', email: '' });
              setFormError(null);
            })
            .catch(error => {
              setError(t('voluntariado.errorRegistering'));
            });
        }
      })
      .catch(error => {
        setError(t('voluntariado.errorCheckingEmails'));
      });
  };

  const openModal = (opportunity) => {
    setSelectedOpportunity(opportunity);
    setShowModal(true);
    setRegistrationSuccess(null);
    setFormError(null);
  };

  const handleClose = () => {
    setShowModal(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('voluntariado.loading')}</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!oportunidades || oportunidades.length === 0) {
    return <p className="text-center">{t('voluntariado.noOpportunitiesFound')}</p>;
  }

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 className="text-center" style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700' }}>
          {t('voluntariado.title')}
        </h1>
        <p className="text-center" style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000' }}>
          {t('voluntariado.description')}
        </p>
        {oportunidades.map(oportunidade => (
          <div key={oportunidade.id}>
            <Row className="my-4 align-items-center">
              <Col md={8}>
                <h5 style={{ fontWeight: 'bold', color: '#333' }}>{oportunidade.title || t('voluntariado.noTitle')}</h5>
                <p style={{ margin: '0.5rem 0', color: '#555' }}>
                  <strong>{t('voluntariado.location')}:</strong> {oportunidade.location || t('voluntariado.noLocation')}
                </p>
                <p style={{ margin: '0.5rem 0', color: '#555' }}>
                  <strong>{t('voluntariado.date')}:</strong> {oportunidade.date || t('voluntariado.noDate')}
                </p>
                <p style={{ margin: '0.5rem 0', color: '#555' }}>
                  <strong>{t('voluntariado.description')}:</strong> {oportunidade.description || t('voluntariado.noDescription')}
                </p>
              </Col>
              <Col md={4} className="text-md-right text-center">
                <Button variant="success" onClick={() => openModal(oportunidade)}>
                  {t('voluntariado.register')}
                </Button>
              </Col>
            </Row>
            <hr />
          </div>
        ))}

        <Modal show={showModal} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>{t('voluntariado.registerFor')} {selectedOpportunity?.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {registrationSuccess ? (
              <Alert variant="success">{registrationSuccess}</Alert>
            ) : (
              <Form>
                <Form.Group controlId="formName">
                  <Form.Label>{t('voluntariado.name')}</Form.Label>
                  <Form.Control 
                    type="text" 
                    placeholder={t('voluntariado.placeholderName')} 
                    name="name" 
                    value={formData.name} 
                    onChange={handleChange} 
                    isInvalid={formError && formError.includes('Name')}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formError && formError.includes('Name') ? formError : null}
                  </Form.Control.Feedback>
                </Form.Group>
                <Form.Group controlId="formEmail" className="mt-3">
                  <Form.Label>{t('voluntariado.email')}</Form.Label>
                  <Form.Control 
                    type="email" 
                    placeholder={t('voluntariado.placeholderEmail')} 
                    name="email" 
                    value={formData.email} 
                    onChange={handleChange} 
                    isInvalid={formError && formError.includes('Email')}
                  />
                  <Form.Control.Feedback type="invalid">
                    {formError && formError.includes('Email') ? formError : null}
                  </Form.Control.Feedback>
                </Form.Group>
              </Form>
            )}
          </Modal.Body>
          {!registrationSuccess && (
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                {t('voluntariado.cancel')}
              </Button>
              <Button variant="success" onClick={() => handleRegister(selectedOpportunity.id)}>
                {t('voluntariado.confirmRegistration')}
              </Button>
            </Modal.Footer>
          )}
        </Modal>
      </Container>
      <Footer />
    </div>
  );
}

export default Voluntariado;
