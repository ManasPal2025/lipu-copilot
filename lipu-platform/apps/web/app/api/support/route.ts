import { NextResponse } from 'next/server';

import { addComplaint } from '@/lib/support-store';
import { ISSUE_TYPES, PRODUCT_TYPES } from '@/lib/support-types';

const MAX_IMAGE_BYTES = 4 * 1024 * 1024;
const ALLOWED_IMAGE_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);

function isValidOption(value: string, options: readonly { value: string }[]): boolean {
  return options.some((option) => option.value === value);
}

export async function POST(request: Request) {
  try {
    const formData = await request.formData();

    const name = String(formData.get('name') ?? '').trim();
    const phone = String(formData.get('phone') ?? '').trim();
    const productType = String(formData.get('productType') ?? '').trim();
    const issueType = String(formData.get('issueType') ?? '').trim();
    const description = String(formData.get('description') ?? '').trim();
    const imageFile = formData.get('image');

    if (!name || name.length < 2) {
      return NextResponse.json({ error: 'Please enter your name.' }, { status: 400 });
    }

    if (!phone || phone.replace(/\D/g, '').length < 10) {
      return NextResponse.json({ error: 'Please enter a valid phone number.' }, { status: 400 });
    }

    if (!isValidOption(productType, PRODUCT_TYPES)) {
      return NextResponse.json({ error: 'Please select a product type.' }, { status: 400 });
    }

    if (!isValidOption(issueType, ISSUE_TYPES)) {
      return NextResponse.json({ error: 'Please select an issue type.' }, { status: 400 });
    }

    if (!description || description.length < 10) {
      return NextResponse.json({ error: 'Please describe the issue in at least 10 characters.' }, { status: 400 });
    }

    let imageMeta: { name: string; type: string; size: number } | undefined;

    if (imageFile instanceof File && imageFile.size > 0) {
      if (!ALLOWED_IMAGE_TYPES.has(imageFile.type)) {
        return NextResponse.json(
          { error: 'Photo must be a JPG, PNG, or WebP file.' },
          { status: 400 },
        );
      }

      if (imageFile.size > MAX_IMAGE_BYTES) {
        return NextResponse.json({ error: 'Photo must be smaller than 4 MB.' }, { status: 400 });
      }

      imageMeta = {
        name: imageFile.name,
        type: imageFile.type,
        size: imageFile.size,
      };
    }

    const record = addComplaint({
      name,
      phone,
      productType,
      issueType,
      description,
      image: imageMeta,
    });

    return NextResponse.json({
      ticketNumber: record.ticketNumber,
      message: 'Your message has been received. Our support team will call you within one business day.',
      createdAt: record.createdAt,
    });
  } catch {
    return NextResponse.json({ error: 'Something went wrong. Please try again.' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    message: 'LIPU support mock API — POST multipart form data to submit a complaint.',
  });
}
