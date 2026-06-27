# Welcome to Datalab

Datalab provides document intelligence APIs to convert PDFs, spreadsheets, images, and other formats into structured, machine-readable outputs — fast, accurately, and at scale.

We offer a [fully managed platform](./docs/welcome/api), [on-prem deployment](./docs/on-prem/overview) for sensitive documents, and open-source tools for developers. **New accounts include \$5 in free credits** — [sign up here](https://www.datalab.to/auth/sign_up).

## Key Capabilities

* **Document Conversion** — Parse PDFs, Word docs, and spreadsheets into Markdown, HTML, or JSON (powered by [Marker](https://github.com/datalab-to/marker), [Surya](https://github.com/datalab-to/surya), and [Chandra](https://github.com/datalab-to/chandra))
* **Pipelines** — Chain processors into versioned, reusable configurations and deploy to production
* **Structured Extraction** — Extract specific fields with citations back to source bounding boxes for auditability
* **Form Filling** — Automatically fill PDF and image forms with structured data
* **Document Segmentation** — Split multi-document PDFs into separate logical sections
* **Track Changes** — Extract redlines and comments from Word documents
* **OCR** — High-accuracy text recognition supporting 90+ languages

## What do you want to do?

**Convert documents to structured formats**
→ [Document Conversion](./docs/recipes/conversion/conversion-api-overview)

**Extract specific data from documents**
→ [Structured Extraction](./docs/recipes/structured-extraction/api-overview)

**Automatically fill PDF forms**
→ [Form Filling](./docs/recipes/form-filling/form-filling-api-overview)

**Split combined PDFs into separate documents**
→ [Document Segmentation](./docs/recipes/document-segmentation/auto-segmentation)

**Build document processing pipelines**
→ [Pipelines](./docs/recipes/pipelines/pipeline-overview)

**Extract tracked changes from Word documents**
→ [Track Changes](./docs/recipes/extract-redlines-and-comments/track-changes-from-word-documents)

## Who uses Datalab?

Datalab serves teams building AI agents, RAG systems, and document automation workflows:

* **AI/ML teams** — Feed knowledge graphs, retrieval systems, and automation pipelines with clean, structured document data
* **Enterprises** — Automate high-volume document processing with auditability and citation tracking
* **Product teams** — Convert financial statements, legal filings, tax forms, and research papers into product-ready content

## Getting Started

<CardGroup cols={2}>
  <Card title="SDK Quickstart" icon="rocket" href="/docs/welcome/quickstart">
    Start converting documents in minutes with Python.
  </Card>

  <Card title="API Reference" icon="bolt" href="/docs/welcome/api">
    REST API documentation.
  </Card>

  <Card title="Build a Pipeline" icon="workflow" href="/docs/recipes/pipelines/pipeline-overview">
    Chain processors into versioned, reusable pipelines.
  </Card>

  <Card title="Open Source" icon="github" href="https://github.com/datalab-to">
    Run our models locally.
  </Card>
</CardGroup>

## Support

<CardGroup cols={2}>
  <Card title="Contact Support" icon="circle-question">
    Email [support@datalab.to](mailto:support@datalab.to) for help.
  </Card>

  <Card title="Service Status" icon="chart-line" href="https://status.datalab.to/">
    Check API availability.
  </Card>
</CardGroup>