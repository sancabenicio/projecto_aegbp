import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from './Header';
import { Container, Form, Button, Card, Alert, ListGroup } from 'react-bootstrap';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import Footer from './Footer'; 
import './BlogPost.css';

const BlogPost = () => {
  const { t, i18n } = useTranslation(); // Incluindo i18n para obter o idioma atual
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [comment, setComment] = useState({ name: '', content: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [formErrors, setFormErrors] = useState({});

  const getCSRFToken = () => {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        return cookie.substring(name.length + 1);
      }
    }
    return null;
  };

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/blogposts/${id}/`;

    axios.get(apiUrl)
      .then(response => {
        const post = {
          ...response.data,
          title: response.data[`title_${i18n.language}`] || response.data.title,
          content: response.data[`content_${i18n.language}`] || response.data.content,
        };
        setPost(post);
        setLoading(false);
      })
      .catch(error => {
        console.error('Erro ao buscar o post:', error);
        setError(t('blog.errorFetchingPosts'));
        setLoading(false);
      });

    const commentsUrl = `http://localhost:8000/${languagePrefix}/api/comments/?post=${id}`;
    axios.get(commentsUrl)
      .then(response => {
        setComments(response.data);
      })
      .catch(error => {
        console.error('Erro ao buscar comentários:', error);
      });
  }, [id, t, i18n.language]); // Adicionando i18n.language como dependência

  const validateForm = () => {
    const errors = {};

    if (comment.name.trim().length < 2) {
      errors.name = t('blog.nameError');
    }

    if (comment.content.trim().length < 5) {
      errors.content = t('blog.commentError');
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    const csrfToken = getCSRFToken();
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/comments/`;

    axios.post(apiUrl, {
      post: id,
      author_name: comment.name,
      content: comment.content
    }, {
      headers: {
        'X-CSRFToken': csrfToken,
      }
    })
    .then(response => {
      setComment({ name: '', content: '' });
      setSuccessMessage(t('blog.commentSuccess'));
      setError(null);
      setFormErrors({});

      setComments([...comments, response.data]);
    })
    .catch(error => {
      console.error('Erro ao enviar o comentário:', error);
      setSuccessMessage(null);
      setError(t('blog.commentError'));
    });
  };

  if (loading) {
    return <p>{t('blog.loading')}</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!post) {
    return <p>{t('blog.postNotFound')}</p>;
  }

  return (
    <div>
      <Header />
      <Container className="py-5 blog-post-container">
        <Card className="shadow-sm">
          <Card.Img variant="top" src={post.image} alt={post.title} className="blog-post-image" />
          <Card.Body>
            <Card.Title className="text-center blog-post-title">{post.title}</Card.Title>
            <Card.Subtitle className="mb-2 text-muted text-center blog-post-author_name">
              {post.author_name} - {post.formatted_date}
            </Card.Subtitle>
            <Card.Text className="blog-post-content">
              {post.content}
            </Card.Text>
          </Card.Body>
        </Card>

        <h4 className="mt-5">{t('blog.comments')}</h4>
        <ListGroup variant="flush" className="mb-4">
          {comments.length === 0 ? (
            <p>{t('blog.noCommentsYet')}</p>
          ) : (
            comments.map((comment, index) => (
              <ListGroup.Item key={index}>
                <strong>{comment.author_name}</strong>
                <p>{comment.content}</p>
              </ListGroup.Item>
            ))
          )}
        </ListGroup>

        <h4 className="mt-5">{t('blog.leaveComment')}</h4>
        {successMessage && <Alert variant="success">{successMessage}</Alert>}
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={handleSubmit} className="mt-3">
          <Form.Group className="mb-3" controlId="formBasicName">
            <Form.Label>{t('blog.name')}</Form.Label>
            <Form.Control
              type="text"
              placeholder={t('blog.name')}
              value={comment.name}
              onChange={(e) => setComment({ ...comment, name: e.target.value })}
              className="rounded-pill"
              isInvalid={!!formErrors.name}
              required
            />
            <Form.Control.Feedback type="invalid">
              {formErrors.name}
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicComment">
            <Form.Label>{t('blog.comment')}</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder={t('blog.comment')}
              value={comment.content}
              onChange={(e) => setComment({ ...comment, content: e.target.value })}
              className="rounded"
              isInvalid={!!formErrors.content}
              required
            />
            <Form.Control.Feedback type="invalid">
              {formErrors.content}
            </Form.Control.Feedback>
          </Form.Group>

          <Button variant="primary" type="submit" className="rounded-pill px-4">
            {t('blog.submit')}
          </Button>
        </Form>
      </Container>
      <Footer />
    </div>
  );
}

export default BlogPost;
