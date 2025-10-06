import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react'; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {}
    <Auth0Provider
      domain='dev-uijkelx4yghj3cp4.us.auth0.com'
      clientId="yJns9DGoXOHnZGEyOV9vEJDXhMAXx8iH"              
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: "https://invoices-api"
      }}
    >
      <App />
    </Auth0Provider>
  </React.StrictMode>
);