import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext"
import { Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link } from "react-router-dom";

import '../../styles/forgotpwd.css'

const ForgotPassword = () => {

    /*  This was used to make the NavBar hidden on the SignIn page,
        however it was decided to show. Props were used as argument to this page.
        useEffect(() => {
        props.setCurrentURL('/signin');
      }, []) */

    const { actions } = useContext(Context);
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    const handleClick = async () => {
        let results = await actions.handleForgotPassword(email);
        if (results) {
            navigate("/signin")
        }
    }

    return (
        <>
            <Container className="forgotpwd-container">
                <h3 className="text-center mt-2">Forgot Password</h3>
                <p>Please enter your email address and we will send a password reset link to your email.</p>
                <div>
                    <Form.Group className="mb-3 mt-3" controlId="formBasicEmail">
                        <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} />
                        <Form.Text className="text-muted">
                        </Form.Text>
                    </Form.Group>
                    <button className="form-button mb-3" type="button" onClick={handleClick}>
                        Submit
                    </button>
                </div>
            </Container>
        </>
    );
}

export default ForgotPassword;