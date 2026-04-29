# chatPG Flow Diagram

*   **Diagram Owner:** Lukasz Luszczynski
*   **Update:** 31/07/2025

---

## Actors & Systems

*   **P&G User**
*   **WebBrowser/MSTF Teams App**
*   **Application Gateway**
*   **Azure APIM**
*   **MSTF EntraID**
*   **Ping Federate**
*   **PingID MFA**
*   **ChatPG Frontend**
*   **ChatPG Backend**
*   **Authle**
*   **MSTF Active Directory**
*   **GenAI Platform**

---

## Authentication and Initial Request Flow

1.  **P&G User** (WebBrowser/MSTF Teams App) calls `chatPG service()`.
2.  **WebBrowser/MSTF Teams App** sends `call chatPG service()` to **Application Gateway**.
3.  **Application Gateway** forwards to **Azure APIM**.
4.  **Azure APIM** calls `chatPG service frontend()` on **ChatPG Frontend**.
5.  **ChatPG Frontend** detects `user unauthenticated()` and sends `-> redirectURI` to **Azure APIM**.
6.  **Azure APIM** sends `-> redirectURI` to **WebBrowser/MSTF Teams App**.
7.  **WebBrowser/MSTF Teams App** redirects to `redirectURI (/security/v1/auth/authorize)`.
8.  **WebBrowser/MSTF Teams App** redirects to `login page`.
9.  **WebBrowser/MSTF Teams App** sends `redirect to login form()` to **MSTF EntraID**.
10. **MSTF EntraID** sends `redirect and provide email/email + authenticate/credentials` to **WebBrowser/MSTF Teams App**.
11. **WebBrowser/MSTF Teams App** sends `authenticate/credentials` to **MSTF EntraID**.
12. **MSTF EntraID** sends `redirect to PingID (authorization_code)` to **WebBrowser/MSTF Teams App**.
13. **WebBrowser/MSTF Teams App** sends `redirect to PingID (authorization_code)` to **Ping Federate**.
14. **Ping Federate** initiates a step for **PingID MFA**.
15. **Ping Federate** sends `saml assertion()` to **MSTF EntraID**.
16. **MSTF EntraID** sends `saml assertion()` with `authorization_code` to **Ping Federate**.
    *   *Note: Auth is done with Entra ID and Federated with Ping because of lack of generation of token on behalf of user.*
17. **Ping Federate** sends `send authorization code (authorization_code) -> access_token, refresh_token, login` to **ChatPG Frontend**.
18. **ChatPG Frontend** sends `check user group(s)/login` to **Authle**.
19. **Authle** returns `validation_result`.
20. **ChatPG Frontend** sends `check user group(s)/login` to **MSTF Active Directory**.
21. **MSTF Active Directory** returns `get_user_group(login)`.
22. **Authle** sends `store (access_token, refresh_token)`.

---

## JWT Token and Backend Interaction

1.  **ChatPG Frontend** sends `get JWT token (login, user_groups)` to **Authle**.
2.  **Authle** returns `JWT_token`.
3.  **ChatPG Frontend** sends `JWT_token` to **WebBrowser/MSTF Teams App**.
4.  **WebBrowser/MSTF Teams App** sends `call chatPG service/JWT_token` to **Application Gateway**.
5.  **Application Gateway** forwards to **Azure APIM**.
6.  **Azure APIM** calls `chatPG service frontend(JWT_token)` on **ChatPG Frontend**.
7.  **ChatPG Frontend** sends `call chatPG service(JWT_token)` to **ChatPG Backend**.
8.  **ChatPG Backend** sends `check access (JWT_token)` to **Authle**.
9.  **Authle** sends `get Public Key(), Validate token signature(Public_Key)` to **ChatPG Backend**.
10. **Authle** returns `validation_result`.
11. **ChatPG Backend** sends `application_page` to **ChatPG Frontend**.
12. **ChatPG Frontend** sends `application_page` to **Azure APIM**.
13. **Azure APIM** sends `application_page` to **WebBrowser/MSTF Teams App**.
14. **WebBrowser/MSTF Teams App** sends `call chatPG from client side/JWT_token, prompt` to **Application Gateway**.
15. **Application Gateway** forwards to **Azure APIM**.
16. **Azure APIM** calls `chatPG from client side/JWT_token, prompt` on **ChatPG Frontend**.
17. **ChatPG Frontend** sends `call chatPG from client side/JWT_token, prompt` to **ChatPG Backend**.
18. **ChatPG Backend** sends `authorised with Application Credentials(chatpg_app_credentials)` to **GenAI Platform**.
19. **GenAI Platform** sends `prompt GenAI platform(prompt)` to **ChatPG Backend**.
20. **ChatPG Backend** returns `results` to **ChatPG Frontend**.
21. **ChatPG Frontend** returns `results` to **Azure APIM**.
22. **Azure APIM** returns `results` to **WebBrowser/MSTF Teams App**.
