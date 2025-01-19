import { z } from 'zod';

export const supportRequestSchema = z.object({
  fullName: z.string().min(1, 'Full Name is required'),
  email: z.string().email('Invalid email address'),
  issueType: z.string().min(1, 'Please select an issue type'),
  tags: z.array(z.string()).min(1, 'Please select at least one tag'),
  steps: z.array(z.string().min(1, 'Step description is required')),
});
