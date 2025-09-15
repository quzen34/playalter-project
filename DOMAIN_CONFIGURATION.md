# PLAYALTER Domain Configuration

## Production Domain
- **Primary Domain**: www.playalter.com
- **Secondary Domain**: playalter.com (redirects to www)
- **Development**: localhost:5173

## Domain Setup Checklist

### 1. DNS Configuration
- [ ] A Record: playalter.com → Vercel IP
- [ ] CNAME Record: www.playalter.com → playalter.vercel.app
- [ ] Verify domain ownership in Vercel dashboard

### 2. SSL Certificate
- [ ] Auto-provisioned by Vercel
- [ ] HTTPS redirection enabled
- [ ] Security headers configured

### 3. Vercel Configuration
- [x] vercel.json updated with domain aliases
- [x] CORS headers configured for production
- [x] Redirects: playalter.com → www.playalter.com
- [x] Security headers added

### 4. Frontend Configuration
- [x] API_CONFIG updated with production URLs
- [x] Environment variables configured
- [x] HTTP service created for API calls

### 5. Backend Configuration  
- [x] CORS updated for production domain
- [x] Environment variables support

## Environment Variables

### Frontend (.env)
```
VITE_DOMAIN=www.playalter.com
VITE_FRONTEND_URL=https://www.playalter.com
VITE_API_BASE_URL=https://www.playalter.com/api
```

### Backend (.env)
```
FRONTEND_URL=https://www.playalter.com
ALLOWED_ORIGINS=https://www.playalter.com,https://playalter.com
```

## Security Configuration

### Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

### CORS
- Origin: https://www.playalter.com
- Credentials: true
- Methods: GET, POST, PUT, DELETE, OPTIONS

## Testing

### Development
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- API: http://localhost:5000/api/*

### Production
- Frontend: https://www.playalter.com
- Backend: https://www.playalter.com/api
- Health: https://www.playalter.com/api/health

## Deployment Steps

1. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

2. **Add Custom Domain**
   ```bash
   vercel domains add www.playalter.com
   vercel domains add playalter.com
   ```

3. **Configure DNS**
   - Update DNS records at domain registrar
   - Point to Vercel nameservers or IPs

4. **Verify SSL**
   - Check HTTPS accessibility
   - Verify certificate validity

## Post-Deployment Verification

- [ ] https://www.playalter.com loads
- [ ] https://playalter.com redirects to www
- [ ] API endpoints respond correctly
- [ ] CORS working for all origins
- [ ] SSL certificate active
- [ ] Security headers present
