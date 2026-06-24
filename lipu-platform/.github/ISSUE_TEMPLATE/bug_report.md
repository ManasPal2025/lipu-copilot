name: Bug Report
description: Report a bug
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please fill out this form as thoroughly as possible.

  - type: input
    id: title
    attributes:
      label: Title
      description: Brief description of the bug
      placeholder: "Button click not working on mobile"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Detailed description of the bug
      placeholder: "When I click the submit button on mobile devices, nothing happens..."
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Reproduction Steps
      description: Steps to reproduce the bug
      placeholder: |
        1. Navigate to /products
        2. Scroll to bottom
        3. Click the load more button
        4. See error in console
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      placeholder: "The page should load more products"
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      placeholder: "Console shows a 500 error"
    validations:
      required: true

  - type: input
    id: os
    attributes:
      label: Operating System
      placeholder: "Windows 11, macOS 14.0, Ubuntu 23.04"

  - type: input
    id: browser
    attributes:
      label: Browser
      placeholder: "Chrome 120, Firefox 121, Safari 17"

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      placeholder: "Any other information that might help"
