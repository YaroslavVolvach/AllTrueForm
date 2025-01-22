import { supportRequestSchema } from '../components/Form/validationSchema';

describe('Support Request Schema Validation', () => {
  test('validates that full_name is required', () => {
    const result = supportRequestSchema.safeParse({
      email: 'user@example.com',
      issueType: 'bug_report',
      tagIds: [1],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe('Required');
  });

  test('validates that email must be valid', () => {
    const result = supportRequestSchema.safeParse({
      full_name: 'John Doe',
      email: 'invalid-email',
      issueType: 'bug_report',
      tagIds: [1],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe('Invalid email address');
  });

  test('validates that at least one tag is selected', () => {
    const result = supportRequestSchema.safeParse({
      full_name: 'John Doe',
      email: 'user@example.com',
      issueType: 'bug_report',
      tagIds: [],
      steps: ['Step 1'],
    });

    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe(
      'Please select at least one tag'
    );
  });

  test('validates successful input', () => {
    const result = supportRequestSchema.safeParse({
      full_name: 'John Doe',
      email: 'user@example.com',
      issueType: 'bug_report',
      tagIds: [1, 2],
      steps: ['Step 1', 'Step 2'],
    });

    expect(result.success).toBe(true);
  });
});
