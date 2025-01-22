import { z } from 'zod';

export const supportRequestSchema = z.object({
  full_name: z.string().min(1, 'Full Name is required'),
  email: z.string().email('Invalid email address'),
  issueType: z.string().min(1, 'Please select an issue type'),
  tagIds: z.array(z.number()).min(1, 'Please select at least one tag'),
  steps: z
    .array(z.string().min(1, 'Step description is required'))
    .min(1, 'At least one step is required'),
});
