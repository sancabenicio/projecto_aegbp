import React, { useState, useEffect } from 'react';
import Header from './Header';
import { Container, Form, Button, Spinner, Alert, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import Footer from './Footer'; 
import { useTranslation } from 'react-i18next';

const Doacoes = () => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({ name: '', email: '', amount: '', description: '', proof: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [paymentInfo, setPaymentInfo] = useState({ iban: '', mbWay: '' });

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/general-settings/`;

    axios.get(apiUrl)
      .then(response => {
        if (response.data && response.data.length > 0) {
          setPaymentInfo({
            iban: response.data[0].iban,
            mbWay: response.data[0].mb_way_number,
          });
        }
      })
      .catch(error => {
        console.error(t('donations.errorFetchingPaymentInfo'), error);
      });
  }, [t]);

  const validateForm = () => {
    const { name, email, amount, proof } = formData;

    if (!name || !email || !amount) {
      setError(t('donations.errorMandatoryFields'));
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError(t('donations.errorInvalidEmail'));
      return false;
    }

    if (amount <= 0) {
      setError(t('donations.errorInvalidAmount'));
      return false;
    }

    if (proof && !['image/jpeg', 'image/png', 'application/pdf'].includes(proof.type)) {
      setError(t('donations.errorInvalidProofFileType'));
      return false;
    }

    setError(null);
    return true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, proof: e.target.files[0] });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/donations/`;

    const donationData = new FormData();
    donationData.append('name', formData.name);
    donationData.append('email', formData.email);
    donationData.append('amount', formData.amount);
    donationData.append('description', formData.description);
    donationData.append('date', new Date().toISOString().split('T')[0]); 
    if (formData.proof) {
      donationData.append('proof', formData.proof);
    }

    axios.post(apiUrl, donationData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(response => {
        setSuccess(t('donations.successMessage'));
        setFormData({ name: '', email: '', amount: '', description: '', proof: null });
        setLoading(false);
      })
      .catch(error => {
        console.error(t('donations.errorSendingDonation'), error);
        setError(t('donations.errorSendingDonation'));
        setLoading(false);
      });
  };

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center', marginBottom: '2rem' }}>
          {t('donations.title')}
        </h1>
        
        <Row className="mb-5">
          <Col md={6}>
            <div style={{ padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
              <h4 style={{ color: '#333', fontWeight: 'bold', marginBottom: '1rem' }}>{t('donations.paymentInfoTitle')}</h4>
              <p><strong>{t('donations.iban')}:</strong> {paymentInfo.iban}</p>
              <p><strong>{t('donations.mbWay')}:</strong> {paymentInfo.mbWay}</p>
            </div>
          </Col>

          <Col md={6}>
            <div style={{ padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
              <h4 style={{ color: '#333', fontWeight: 'bold', marginBottom: '1rem' }}>{t('donations.formTitle')}</h4>
              <Form onSubmit={handleSubmit}>
                {error && <Alert variant="danger">{error}</Alert>}
                {success && <Alert variant="success">{success}</Alert>}
                <Form.Group controlId="formName" className="mb-3">
                  <Form.Label>{t('donations.name')}</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder={t('donations.namePlaceholder')}
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
                <Form.Group controlId="formEmail" className="mb-3">
                  <Form.Label>{t('donations.email')}</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder={t('donations.emailPlaceholder')}
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
                <Form.Group controlId="formAmount" className="mb-3">
                  <Form.Label>{t('donations.amount')}</Form.Label>
                  <Form.Control
                    type="number"
                    placeholder={t('donations.amountPlaceholder')}
                    name="amount"
                    value={formData.amount}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
                <Form.Group controlId="formDescription" className="mb-3">
                  <Form.Label>{t('donations.description')}</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder={t('donations.descriptionPlaceholder')}
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                  />
                </Form.Group>
                <Form.Group controlId="formProof" className="mb-3">
                  <Form.Label>{t('donations.proof')}</Form.Label>
                  <Form.Control
                    type="file"
                    name="proof"
                    onChange={handleFileChange}
                    accept=".jpg,.jpeg,.png,.pdf"
                  />
                </Form.Group>
                <Button variant="success" type="submit" disabled={loading} style={{ width: '100%' }}>
                  {loading ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : t('donations.submitButton')}
                </Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
      <Footer />
    </div>
  );
};

export default Doacoes;
