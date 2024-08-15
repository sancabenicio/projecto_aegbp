import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import { FaMapMarkerAlt, FaPhoneAlt, FaEnvelope, FaClock } from 'react-icons/fa';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const Contatos = () => {
  const { t, i18n } = useTranslation(); // Incluindo i18n para obter o idioma atual
  const [contactInfo, setContactInfo] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const [status, setStatus] = useState({
    loading: false,
    success: null,
    error: null,
  });

  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/contact-info/`;

    axios.get(apiUrl)
      .then(response => {
        const info = {
          ...response.data[0],
          address: response.data[0][`address_${i18n.language}`] || response.data[0].address,
          phone1: response.data[0][`phone1_${i18n.language}`] || response.data[0].phone1,
          phone2: response.data[0][`phone2_${i18n.language}`] || response.data[0].phone2,
          email1: response.data[0][`email1_${i18n.language}`] || response.data[0].email1,
          email2: response.data[0][`email2_${i18n.language}`] || response.data[0].email2,
          days_of_week: response.data[0][`days_of_week_${i18n.language}`] || response.data[0].days_of_week,
          hours: response.data[0][`hours_${i18n.language}`] || response.data[0].hours,
        };
        setContactInfo(info);
      })
      .catch(error => {
        console.error(t('contact.errorFetchingInfo'), error);
      });
  }, [t, i18n.language]); // Adicionando i18n.language como dependência

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  const validateForm = () => {
    const errors = {};

    if (formData.name.trim().length < 2) {
      errors.name = t('contact.nameError');
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      errors.email = t('contact.emailError');
    }

    if (formData.subject.trim().length < 3) {
      errors.subject = t('contact.subjectError');
    }

    if (formData.message.trim().length < 10) {
      errors.message = t('contact.messageError');
    }

    setFormErrors(errors);

    return Object.keys(errors).length === 0;
  };

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    setStatus({ loading: true, success: null, error: null });

    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/contact-messages/`;

    axios.post(apiUrl, formData)
      .then(response => {
        setStatus({ loading: false, success: t('contact.successMessage'), error: null });
        setFormData({
          name: '',
          email: '',
          subject: '',
          message: ''
        });
        setFormErrors({});
      })
      .catch(error => {
        console.error(t('contact.errorSendingMessage'), error);
        setStatus({ loading: false, success: null, error: t('contact.errorSendingMessage') });
      });
  };

  return (
    <div>
      <Container className="py-5">
        <h1 className="text-center" style={{ fontWeight: 'bold', color: '#006400' }}>
          {t('contact.title')}
        </h1>
        <p className="text-center mb-5" style={{ color: '#666' }}>
          {t('contact.subtitle')}
        </p>
        <Row>
          <Col md={6} className="mb-4">
            <Row>
              <Col md={6} className="d-flex align-items-stretch">
                <div className="info-box w-100 p-3 text-center">
                  <FaMapMarkerAlt size={40} color="#006400" />
                  <h4 className="mt-3" style={{ fontWeight: 'bold', color: '#333' }}>{t('contact.address')}</h4>
                  <p style={{ color: '#666' }}>{contactInfo?.address || t('contact.noAddress')}</p>
                </div>
              </Col>
              <Col md={6} className="d-flex align-items-stretch">
                <div className="info-box w-100 p-3 text-center">
                  <FaPhoneAlt size={40} color="#006400" />
                  <h4 className="mt-3" style={{ fontWeight: 'bold', color: '#333' }}>{t('contact.phone')}</h4>
                  <p style={{ color: '#666' }}>
                    {contactInfo?.phone1 || t('contact.noPhone')}
                    <br />
                    {contactInfo?.phone2 || ''}
                  </p>
                </div>
              </Col>
              <Col md={6} className="d-flex align-items-stretch">
                <div className="info-box w-100 p-3 text-center">
                  <FaEnvelope size={40} color="#006400" />
                  <h4 className="mt-3" style={{ fontWeight: 'bold', color: '#333' }}>{t('contact.email')}</h4>
                  <p style={{ color: '#666' }}>
                    {contactInfo?.email1 || t('contact.noEmail')}
                    <br />
                    {contactInfo?.email2 || ''}
                  </p>
                </div>
              </Col>
              <Col md={6} className="d-flex align-items-stretch">
                <div className="info-box w-100 p-3 text-center">
                  <FaClock size={40} color="#006400" />
                  <h4 className="mt-3" style={{ fontWeight: 'bold', color: '#333' }}>{t('contact.hours')}</h4>
                  <p style={{ color: '#666' }}>
                    {contactInfo?.days_of_week || t('contact.noDays')}
                    <br />
                    {contactInfo?.hours || t('contact.noHours')}
                  </p>
                </div>
              </Col>
            </Row>
          </Col>
          <Col md={6}>
            <Form onSubmit={handleSubmit}>
              <Row>
                <Col md={6} className="mb-3">
                  <Form.Group controlId="name">
                    <Form.Control
                      type="text"
                      placeholder={t('contact.yourName')}
                      value={formData.name}
                      onChange={handleChange}
                      isInvalid={!!formErrors.name}
                      required
                    />
                    <Form.Control.Feedback type="invalid">
                      {formErrors.name}
                    </Form.Control.Feedback>
                  </Form.Group>
                </Col>
                <Col md={6} className="mb-3">
                  <Form.Group controlId="email">
                    <Form.Control
                      type="email"
                      placeholder={t('contact.yourEmail')}
                      value={formData.email}
                      onChange={handleChange}
                      isInvalid={!!formErrors.email}
                      required
                    />
                    <Form.Control.Feedback type="invalid">
                      {formErrors.email}
                    </Form.Control.Feedback>
                  </Form.Group>
                </Col>
              </Row>
              <Form.Group controlId="subject" className="mb-3">
                <Form.Control
                  type="text"
                  placeholder={t('contact.subject')}
                  value={formData.subject}
                  onChange={handleChange}
                  isInvalid={!!formErrors.subject}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  {formErrors.subject}
                </Form.Control.Feedback>
              </Form.Group>
              <Form.Group controlId="message" className="mb-3">
                <Form.Control
                  as="textarea"
                  rows={5}
                  placeholder={t('contact.message')}
                  value={formData.message}
                  onChange={handleChange}
                  isInvalid={!!formErrors.message}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  {formErrors.message}
                </Form.Control.Feedback>
              </Form.Group>
              <Button variant="primary" type="submit" disabled={status.loading}>
                {status.loading ? t('contact.sending') : t('contact.sendMessage')}
              </Button>
            </Form>
            {status.success && <Alert variant="success" className="mt-3">{status.success}</Alert>}
            {status.error && <Alert variant="danger" className="mt-3">{status.error}</Alert>}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Contatos;
