import { supportRequestSchema } from '../components/Form/validationSchema';

describe('Validation Schema', () => {
  test('validates that fullName is required', () => {
    const result = supportRequestSchema.safeParse({
      fullName: '',
      email: 'test@example.com',
      issueType: 'bug',
      tags: ['UI'],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe('Full Name is required');
  });

  test('validates that email must be valid', () => {
    const result = supportRequestSchema.safeParse({
      fullName: 'John Doe',
      email: 'invalid-email',
      issueType: 'bug',
      tags: ['UI'],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe('Invalid email address');
  });

  test('validates successful input', () => {
    const result = supportRequestSchema.safeParse({
      fullName: 'John Doe',
      email: 'john.doe@example.com',
      issueType: 'bug',
      tags: ['UI', 'Performance'],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(true);
  });

  test('validates that at least one step is required', () => {
    const result = supportRequestSchema.safeParse({
      fullName: 'John Doe',
      email: 'john.doe@example.com',
      issueType: 'bug',
      tags: ['UI'],
      steps: [],
    });

    console.log(result);
    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe(
      'At least one step is required'
    );
  });
});
