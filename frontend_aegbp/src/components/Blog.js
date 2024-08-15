import React, { useState, useEffect } from 'react';
import { Container, Card, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import './Blog.css';

const Blog = () => {
  const [blogPosts, setBlogPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { t, i18n } = useTranslation(); // Incluindo i18n para obter o idioma atual

  // Função para extrair o prefixo de idioma da URL
  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//); // Captura o primeiro segmento do caminho
    return match ? match[1] : 'en'; // Retorna 'en' como padrão se não encontrar
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/blogposts/`;

    axios.get(apiUrl)
      .then(response => {
        const posts = response.data.map(post => ({
          ...post,
          title: post[`title_${i18n.language}`] || post.title,
          excerpt: post[`excerpt_${i18n.language}`] || post.excerpt,
          content: post[`content_${i18n.language}`] || post.content,
        }));
        setBlogPosts(posts);
        setLoading(false);
      })
      .catch(error => {
        console.error(t('blog.errorFetchingPosts'), error);
        setError(t('blog.errorFetchingPosts'));
        setLoading(false);
      });
  }, [t, i18n.language]); // Adicionando i18n.language como dependência

  if (loading) {
    return <p>{t('blog.loading')}</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center' }}>
          {t('blog.title')}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000', textAlign: 'center' }}>
          {t('blog.subtitle')}
        </p>
        <Row className="d-flex align-items-stretch">
          {blogPosts.length === 0 ? (
            <p>{t('blog.noPostsFound')}</p> 
          ) : (
            blogPosts.map(post => (
              <Col md={4} className="mb-4 d-flex align-items-stretch" key={post.id}>
                <Card className="w-100 h-100">
                  <Card.Img variant="top" src={post.image} alt={post.title} />
                  <Card.Body className="d-flex flex-column">
                    <Card.Subtitle className="mb-2 text-muted">{post.category}</Card.Subtitle>
                    <Card.Title>{post.title}</Card.Title>
                    <Card.Text className="flex-grow-1">{post.excerpt}</Card.Text>
                    <Link to={`/blog/${post.id}`} className="stretched-link mt-auto">
                      {t('blog.readMore')}
                    </Link>
                  </Card.Body>
                  <Card.Footer>
                    <small className="text-muted">
                      {post.author_name} - {post.formatted_date}
                    </small>
                  </Card.Footer>
                </Card>
              </Col>
            ))
          )}
        </Row>
      </Container>
    </div>
  );
}

export default Blog;
