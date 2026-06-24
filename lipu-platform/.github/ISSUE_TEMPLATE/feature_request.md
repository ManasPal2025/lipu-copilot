name: Feature Request
description: Suggest a new feature
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting a feature! Please describe what you'd like to see.

  - type: input
    id: title
    attributes:
      label: Feature Title
      placeholder: "Add product comparison feature"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the feature and why it would be useful
      placeholder: "Users should be able to compare up to 3 products side-by-side to make better decisions..."
    validations:
      required: true

  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      placeholder: "As a customer, I want to..."
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      placeholder: "Other ways this could be solved..."
