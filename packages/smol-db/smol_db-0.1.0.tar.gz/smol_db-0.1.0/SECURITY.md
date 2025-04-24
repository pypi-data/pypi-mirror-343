# Security Policy

## Supported Versions

We currently support the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within smol-db, please send an email to small.joshua@gmail.com. All security vulnerabilities will be promptly addressed.

Please include the following information in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

## Security Considerations

### Data Storage

- smol-db uses smol-format for data storage, which provides:
  - Exact preservation of rational numbers
  - Efficient compression
  - Type validation
- smol-db does not encrypt data by default
- Consider encrypting sensitive data before storage

### Access Control

- smol-db is a library and does not implement access control
- Implement appropriate access control in your application
- Consider using file system permissions for data files

### Data Validation

- smol-db validates data types but not content
- Implement additional validation as needed
- Be careful with user-provided data

## Best Practices

1. Keep smol-db and its dependencies up to date
2. Use appropriate file system permissions
3. Implement application-level security measures
4. Regularly audit your data
5. Back up your data regularly