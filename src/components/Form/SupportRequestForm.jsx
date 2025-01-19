import React from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { supportRequestSchema } from './validationSchema';
import { useDispatch } from 'react-redux';
import { saveFormData } from '../../redux/slices/formSlice';
import { useNavigate } from 'react-router-dom';

const SupportRequestForm = () => {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(supportRequestSchema),
    defaultValues: {
      fullName: '',
      email: '',
      issueType: '',
      tags: [],
      steps: [''],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'steps',
  });

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onSubmit = (data) => {
    dispatch(saveFormData(data));
    navigate('/confirmation');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Full Name Field */}
      <div>
        <label>Full Name</label>
        <input {...register('fullName')} />
        {errors.fullName && <p>{errors.fullName.message}</p>}
      </div>

      {/* Email Address Field */}
      <div>
        <label>Email Address</label>
        <input type="email" {...register('email')} />
        {errors.email && <p>{errors.email.message}</p>}
      </div>

      {/* Issue Type Dropdown */}
      <div>
        <label>Issue Type</label>
        <select {...register('issueType')}>
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
        {errors.tags && <p>{errors.tags.message}</p>}
      </div>

      {/* Steps to Reproduce Dynamic Field */}
      <div>
        <label>Steps to Reproduce</label>
        {fields.map((field, index) => (
          <div key={field.id}>
            <input
              {...register(`steps.${index}`)}
              placeholder={`Step ${index + 1}`}
            />
            {errors.steps?.[index] && <p>{errors.steps[index].message}</p>}
            <button type="button" onClick={() => remove(index)}>
              Remove
            </button>
          </div>
        ))}
        <button type="button" onClick={() => append('')}>
          Add Step
        </button>
      </div>

      {/* Submit Button */}
      <button type="submit">Submit</button>
    </form>
  );
};

export default SupportRequestForm;
