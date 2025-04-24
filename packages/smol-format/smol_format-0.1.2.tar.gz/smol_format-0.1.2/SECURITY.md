# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within smol-format, please send an email to small.joshua@gmail.com. All security vulnerabilities will be promptly addressed.

Please include the following information in your report:
- Type of vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

## Security Considerations

### Data Storage
- smol-format does not encrypt data by default
- Consider encrypting sensitive data before storage
- Use appropriate access controls for stored data

### Compression
- Zstandard compression is not encryption
- Compressed data should not be considered secure
- Use additional encryption for sensitive data

### Input Validation
- smol-format validates data types but not content
- Validate input data before storage
- Be cautious with untrusted data sources

## Best Practices

1. **Data Protection**
   - Encrypt sensitive data before storage
   - Use secure storage locations
   - Implement proper access controls

2. **Input Handling**
   - Validate all input data
   - Sanitize data before storage
   - Use appropriate data types

3. **System Security**
   - Keep dependencies updated
   - Monitor for security advisories
   - Follow security best practices