import React from 'react';
import { useForm, useFieldArray } from 'react-hook-form';

const SupportRequestForm = () => {
  const { register, handleSubmit, control, formState: { errors } } = useForm({
    defaultValues: {
      fullName: '',
      email: '',
      issueType: '',
      tags: [],
      steps: [''], // Default to one step
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'steps', // Dynamic steps field
  });

  const onSubmit = (data) => {
    console.log(data); // Replace with Redux dispatch later
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Full Name Field */}
      <div>
        <label>Full Name</label>
        <input {...register('fullName', { required: 'Full Name is required' })} />
        {errors.fullName && <p>{errors.fullName.message}</p>}
      </div>

      {/* Email Field */}
      <div>
        <label>Email</label>
        <input
          type="email"
          {...register('email', { 
            required: 'Email is required', 
            pattern: { value: /\S+@\S+\.\S+/, message: 'Invalid email address' }
          })}
        />
        {errors.email && <p>{errors.email.message}</p>}
      </div>

      {/* Issue Type Dropdown */}
      <div>
        <label>Issue Type</label>
        <select {...register('issueType', { required: 'Please select an issue type' })}>
          <option value="">Select Issue Type</option>
          <option value="bug">Bug Report</option>
          <option value="feature">Feature Request</option>
          <option value="general">General Inquiry</option>
        </select>
        {errors.issueType && <p>{errors.issueType.message}</p>}
      </div>

      {/* Tags Multi-Select */}
      <div>
        <label>Tags</label>
        <select {...register('tags')} multiple>
          <option value="UI">UI</option>
          <option value="Backend">Backend</option>
          <option value="Performance">Performance</option>
        </select>
      </div>

      {/* Steps to Reproduce */}
      <div>
        <label>Steps to Reproduce</label>
        {fields.map((item, index) => (
          <div key={item.id}>
            <input
              {...register(`steps.${index}`, { required: 'Step description is required' })}
              placeholder={`Step ${index + 1}`}
            />
            {errors.steps?.[index] && <p>{errors.steps[index].message}</p>}
            <button type="button" onClick={() => remove(index)}>Remove</button>
          </div>
        ))}
        <button type="button" onClick={() => append('')}>Add Step</button>
      </div>

      <button type="submit">Submit</button>
    </form>
  );
};

export default SupportRequestForm;