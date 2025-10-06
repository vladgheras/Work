import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import './App.css';


function App() {
  const{
    loginWithRedirect,
    logout,
    user,
    isAuthenticated,
    isLoading,
    getAccessTokenSilently
  } = useAuth0();
          
  const [invoices , setInvoices] = useState(null);

  const getInvoicesFromApi = async () => { 
    try {
      const token = await getAccessTokenSilently();
      console.log("Token obținut de la Auth0:", token);
      const response = await fetch('http://localhost:8000/invoices', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      console.log('API Response:', data); 

      setInvoices(data);
    }
    catch (error) {
      console.error("Error fetching invoices:", error);
    }
  };
  
  if (isLoading) {
    return <div>Loading...</div>;
  }
  return (
    <div className="App">
      <header className="App-header">
        <h1>Auth0 React Example</h1>
        {!isAuthenticated ? (
          <button onClick={() => loginWithRedirect()}>Log in</button>
        ) : (
          <div>
            <button onClick={() => logout({ returnTo: window.location.origin })}>
              Log out
            </button>
            <h2>Welcome, {user.name}</h2>
            <button onClick={getInvoicesFromApi}>Get Invoices</button>
            {Array.isArray(invoices) && invoices.length > 0 ? (
              <div>
                <h3>Your Invoices:</h3>
                <ul>
                  {invoices.map((invoice) => (
                    <li key={invoice.id}>
                      Status: {invoice.status} - ${invoice.amount}
                    </li>
                  ))}
                </ul>
              </div>
            ) : (<p>No invoices found.</p>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
