# Playwright End-to-End Testing for CI/CD

This document explains the Playwright test setup for CI/CD environments, specifically configured to run efficiently in automated pipelines.

## 🚀 Quick Start

### Local Development
```bash
# Run all tests on all browsers (development)
npm run test:e2e

# Run tests on Chrome only (faster)
npm run test:e2e:chrome

# Run tests with UI (debugging)
npm run test:e2e:ui

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Debug specific tests
npm run test:e2e:debug
```

### CI/CD Environment
```bash
# Optimized for CI - Chrome only, no browser UI, proper exit
npm run test:e2e:ci

# View test reports (after tests run)
npm run test:e2e:report
```

## 🔧 Configuration Features

### CI-Optimized Settings

1. **Browser Selection**: 
   - Development: Chrome, Firefox, Safari
   - CI: Chrome only (faster, more reliable)

2. **Reporting**:
   - Development: HTML report (opens automatically)
   - CI: List + JUnit XML (no browser opening)

3. **Timeouts**:
   - Global: 5 minutes total
   - Per test: 30 seconds
   - Server start: 2 minutes

4. **Parallelization**:
   - Development: Full parallel execution
   - CI: Single worker (more stable)

### Test Isolation

- **Unique users**: Each test uses a timestamp-based username to avoid data conflicts
- **Clean state**: Tests clear localStorage before each run
- **Specific locators**: Uses `.first()` selectors to handle multiple elements

## 📋 Test Coverage

### Core User Workflows

1. **Login Flow**
   - Username validation
   - Dashboard redirection
   - Welcome message display

2. **Meal Management**
   - Create meals with nutritional data
   - Form validation (required fields, numeric inputs)
   - Real-time table updates

3. **Data Visualization**
   - Stats display with macro breakdown
   - Responsive chart rendering
   - No-data state handling

4. **CRUD Operations**
   - Delete meals with confirmation
   - Clean up test data
   - UI state consistency

5. **Date Filtering**
   - Filter meal history
   - "Today" vs "All time" views

## 🏗️ CI/CD Integration

### GitHub Actions Example

The provided `.github/workflows/e2e-tests.yml` shows how to:

1. Set up Node.js and Python environments
2. Start the backend API server
3. Install Playwright with browser dependencies
4. Run tests in CI mode
5. Upload test artifacts (reports, traces)

### Key Environment Variables

- `CI=true`: Enables CI-optimized configuration
- Browser selection automatically switches to Chrome-only
- Reports switch to non-interactive mode

### Docker Support

For containerized CI environments:

```dockerfile
# Add to your CI Dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npx playwright install chromium

# Run tests
CMD ["npm", "run", "test:e2e:ci"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: Tests automatically start dev server on port 3000
2. **Backend Dependency**: Ensure backend is running on port 8000
3. **Browser Installation**: Run `npx playwright install` for missing browsers

### Debug Commands

```bash
# View test traces (after failure)
npx playwright show-trace test-results/*/trace.zip

# Run specific test file
npx playwright test meal-workflow.spec.ts

# Run in debug mode
npx playwright test --debug
```

## 📊 Performance Metrics

### Typical Run Times

- **CI Mode (Chrome only)**: ~15-20 seconds
- **Full Mode (3 browsers)**: ~45-60 seconds
- **Single browser development**: ~20-25 seconds

### Resource Usage

- **CI Mode**: Minimal CPU/memory footprint
- **Headless**: No display server required
- **Parallel**: Disabled in CI for stability

## 🔄 Continuous Integration Benefits

1. **Fast Feedback**: Quick test execution in CI
2. **Reliable**: Chrome-only reduces flaky tests
3. **Comprehensive**: Full user journey coverage
4. **Maintainable**: Clear test isolation and cleanup
5. **Debuggable**: Trace files and screenshots on failure

## 📈 Scaling for Larger Teams

### Best Practices

1. **Test Data**: Use unique identifiers to avoid conflicts
2. **Page Objects**: Consider implementing for complex UIs
3. **Test Groups**: Split into smoke, regression, and feature tests
4. **Parallel Execution**: Enable in development, disable in CI

### Future Enhancements

- Visual regression testing
- Cross-browser CI matrix
- Performance testing integration
- Mobile device testing

---

## 🎯 Summary

This Playwright setup provides a robust foundation for CI/CD pipelines with:
- ✅ Fast, reliable CI execution (Chrome-only)
- ✅ Comprehensive local development support (multi-browser)
- ✅ Proper test isolation and cleanup
- ✅ Clear reporting and debugging capabilities
- ✅ Easy integration with popular CI platforms

The tests validate the complete meal tracking workflow from login to data visualization, ensuring your application works end-to-end for real users.
