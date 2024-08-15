import React, { useState, useEffect } from 'react';
import { Container, Form, Button, Alert, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';
import Header from './Header';
import Footer from './Footer';
import { useTranslation } from 'react-i18next';

const RegisterMember = () => {
  const { t } = useTranslation();

  const [formData, setFormData] = useState({
    full_name: '',
    birth_date: '',
    document_number: '',
    document_type: 'PP',
    document_validity: '',
    nationality: '',
    gender: 'M',
    other_gender: '',
    address: '',
    postal_code: '',
    city: '',
    phone: '',
    email: '',
    is_student: false,
    school: '',
    education_type: '',
    course: '',
    academic_year: '',
    is_scholar: false,
    is_working_student: false,
    occupation: '',
  });

  const [existingEmails, setExistingEmails] = useState([]);
  const [existingDocumentNumbers, setExistingDocumentNumbers] = useState([]);
  const [registrationSuccess, setRegistrationSuccess] = useState(null);
  const [registrationError, setRegistrationError] = useState(null);

  useEffect(() => {
    const fetchExistingMembers = async () => {
      try {
        const languagePrefix = getLanguagePrefix();
        const apiUrl = `http://localhost:8000/${languagePrefix}/api/members/`;
        const response = await axios.get(apiUrl);
        const emails = response.data.map(member => member.email);
        const documentNumbers = response.data.map(member => member.document_number);
        setExistingEmails(emails);
        setExistingDocumentNumbers(documentNumbers);
      } catch (error) {
        console.error(t('registerMember.fetchError'), error);
      }
    };
    fetchExistingMembers();
  }, [t]);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const validateForm = () => {
    const { birth_date, postal_code, phone, email, document_number } = formData;

    const age = moment().diff(moment(birth_date, 'YYYY-MM-DD'), 'years');
    if (age < 14) {
      setRegistrationError(t('registerMember.ageError'));
      return false;
    }

    const postalCodeRegex = /^\d{4}-\d{3}$/;
    if (!postalCodeRegex.test(postal_code)) {
      setRegistrationError(t('registerMember.postalCodeError'));
      return false;
    }

    const phoneRegex = /^\d{9}$/;
    if (!phoneRegex.test(phone)) {
      setRegistrationError(t('registerMember.phoneError'));
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setRegistrationError(t('registerMember.emailError'));
      return false;
    }

    if (existingEmails.includes(email)) {
      setRegistrationError(t('registerMember.emailExistsError'));
      return false;
    }

    if (existingDocumentNumbers.includes(document_number)) {
      setRegistrationError(t('registerMember.documentExistsError'));
      return false;
    }

    setRegistrationError(null);
    return true;
  };

  const sendConfirmationEmail = async (email) => {
    try {
      const languagePrefix = getLanguagePrefix();
      const emailUrl = `http://localhost:8000/${languagePrefix}/api/send-email/`;

      const message = t('registerMember.confirmationEmailMessage');

      await axios.post(emailUrl, {
        email,
        subject: t('registerMember.confirmationEmailSubject'),
        message,
      });
    } catch (error) {
      console.error(t('registerMember.emailSendError'), error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/members/`;

    const dataToSubmit = { ...formData };

    if (!formData.is_student) {
      delete dataToSubmit.school;
      delete dataToSubmit.education_type;
      delete dataToSubmit.course;
      delete dataToSubmit.academic_year;
    }

    if (formData.gender !== 'O') {
      delete dataToSubmit.other_gender;
    }

    try {
      await axios.post(apiUrl, dataToSubmit);

      setRegistrationSuccess(t('registerMember.successMessage'));
      setRegistrationError(null);

      await sendConfirmationEmail(formData.email);

      setFormData({
        full_name: '',
        birth_date: '',
        document_number: '',
        document_type: 'PP',
        document_validity: '',
        nationality: '',
        gender: 'M',
        other_gender: '',
        address: '',
        postal_code: '',
        city: '',
        phone: '',
        email: '',
        is_student: false,
        school: '',
        education_type: '',
        course: '',
        academic_year: '',
        is_scholar: false,
        is_working_student: false,
        occupation: '',
      });
    } catch (error) {
      console.error(t('registerMember.registrationError'), error);
      setRegistrationError(t('registerMember.registrationError'));
      setRegistrationSuccess(null);
    }
  };

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 className="text-center" style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700' }}>
          {t('registerMember.title')}
        </h1>
        <p className="text-center" style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000' }}>
          {t('registerMember.subtitle')}
        </p>
        <Form onSubmit={handleSubmit}>
          {registrationSuccess && <Alert variant="success">{registrationSuccess}</Alert>}
          {registrationError && <Alert variant="danger">{registrationError}</Alert>}

          <Row>
            <Col md={6}>
              <Form.Group controlId="formFullName" className="mb-3">
                <Form.Label>{t('registerMember.fullName')}</Form.Label>
                <Form.Control
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formBirthDate" className="mb-3">
                <Form.Label>{t('registerMember.birthDate')}</Form.Label>
                <Form.Control
                  type="date"
                  name="birth_date"
                  value={formData.birth_date}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formDocumentNumber" className="mb-3">
                <Form.Label>{t('registerMember.documentNumber')}</Form.Label>
                <Form.Control
                  type="text"
                  name="document_number"
                  value={formData.document_number}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formDocumentType" className="mb-3">
                <Form.Label>{t('registerMember.documentType')}</Form.Label>
                <Form.Control
                  as="select"
                  name="document_type"
                  value={formData.document_type}
                  onChange={handleChange}
                  required
                >
                  <option value="PP">{t('registerMember.passport')}</option>
                  <option value="CC">{t('registerMember.citizenCard')}</option>
                  <option value="AR">{t('registerMember.residencePermit')}</option>
                </Form.Control>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formDocumentValidity" className="mb-3">
                <Form.Label>{t('registerMember.documentValidity')}</Form.Label>
                <Form.Control
                  type="date"
                  name="document_validity"
                  value={formData.document_validity}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formNationality" className="mb-3">
                <Form.Label>{t('registerMember.nationality')}</Form.Label>
                <Form.Control
                  type="text"
                  name="nationality"
                  value={formData.nationality}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formGender" className="mb-3">
                <Form.Label>{t('registerMember.gender')}</Form.Label>
                <Form.Control
                  as="select"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                >
                  <option value="M">{t('registerMember.male')}</option>
                  <option value="F">{t('registerMember.female')}</option>
                  <option value="O">{t('registerMember.other')}</option>
                </Form.Control>
              </Form.Group>

              {formData.gender === 'O' && (
                <Form.Group controlId="formOtherGender" className="mb-3">
                  <Form.Label>{t('registerMember.otherGender')}</Form.Label>
                  <Form.Control
                    type="text"
                    name="other_gender"
                    value={formData.other_gender}
                    onChange={handleChange}
                  />
                </Form.Group>
              )}
            </Col>
            <Col md={6}>
              <Form.Group controlId="formPhone" className="mb-3">
                <Form.Label>{t('registerMember.phone')}</Form.Label>
                <Form.Control
                  type="text"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formEmail" className="mb-3">
                <Form.Label>{t('registerMember.email')}</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formAddress" className="mb-3">
                <Form.Label>{t('registerMember.address')}</Form.Label>
                <Form.Control
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formPostalCode" className="mb-3">
                <Form.Label>{t('registerMember.postalCode')}</Form.Label>
                <Form.Control
                  type="text"
                  name="postal_code"
                  value={formData.postal_code}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formCity" className="mb-3">
                <Form.Label>{t('registerMember.city')}</Form.Label>
                <Form.Control
                  type="text"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formIsStudent" className="mb-3">
                <Form.Check
                  type="checkbox"
                  label={t('registerMember.isStudent')}
                  name="is_student"
                  checked={formData.is_student}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
            {formData.is_student && (
              <>
                <Col md={6}>
                  <Form.Group controlId="formSchool" className="mb-3">
                    <Form.Label>{t('registerMember.school')}</Form.Label>
                    <Form.Control
                      type="text"
                      name="school"
                      value={formData.school}
                      onChange={handleChange}
                      required={formData.is_student}
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group controlId="formEducationType" className="mb-3">
                    <Form.Label>{t('registerMember.educationType')}</Form.Label>
                    <Form.Control
                      as="select"
                      name="education_type"
                      value={formData.education_type}
                      onChange={handleChange}
                      required={formData.is_student}
                    >
                      <option value="S">{t('registerMember.higherEducation')}</option>
                      <option value="P">{t('registerMember.professionalEducation')}</option>
                      <option value="T">{t('registerMember.secondaryEducation')}</option>
                    </Form.Control>
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group controlId="formCourse" className="mb-3">
                    <Form.Label>{t('registerMember.course')}</Form.Label>
                    <Form.Control
                      type="text"
                      name="course"
                      value={formData.course}
                      onChange={handleChange}
                      required={formData.is_student}
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group controlId="formAcademicYear" className="mb-3">
                    <Form.Label>{t('registerMember.academicYear')}</Form.Label>
                    <Form.Control
                      type="text"
                      name="academic_year"
                      value={formData.academic_year}
                      onChange={handleChange}
                      required={formData.is_student}
                    />
                  </Form.Group>
                </Col>
              </>
            )}
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group controlId="formIsScholar" className="mb-3">
                <Form.Check
                  type="checkbox"
                  label={t('registerMember.isScholar')}
                  name="is_scholar"
                  checked={formData.is_scholar}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="formIsWorkingStudent" className="mb-3">
                <Form.Check
                  type="checkbox"
                  label={t('registerMember.isWorkingStudent')}
                  name="is_working_student"
                  checked={formData.is_working_student}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>

          {!formData.is_student && (
            <Row>
              <Col md={12}>
                <Form.Group controlId="formOccupation" className="mb-3">
                  <Form.Label>{t('registerMember.occupation')}</Form.Label>
                  <Form.Control
                    type="text"
                    name="occupation"
                    value={formData.occupation}
                    onChange={handleChange}
                    required={!formData.is_student}
                  />
                </Form.Group>
              </Col>
            </Row>
          )}

          <Button variant="success" type="submit" style={{ marginTop: '20px', padding: '10px 20px', fontWeight: 'bold' }}>
            {t('registerMember.submitButton')}
          </Button>
        </Form>
      </Container>
      <Footer />
    </div>
  );
};

export default RegisterMember;
