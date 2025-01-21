import React from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { supportRequestSchema } from './validationSchema';
import { useDispatch } from 'react-redux';
import { saveFormData } from '../../redux/slices/formSlice';
import { useNavigate } from 'react-router-dom';
import { FaPlus, FaTimes } from 'react-icons/fa';
import { useSelector } from 'react-redux';
import '../../styles/form.css';

const SupportRequestForm = () => {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
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
  const token = useSelector((state) => state.auth.token);

  const onSubmit = (data) => {
    dispatch(saveFormData(data));
    navigate('/confirmation');
  };

  const steps = watch('steps');

  const handleAddStep = () => {
    append('');
  };

  const isLastStepFilled = steps[steps.length - 1] !== '';

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="fullName">Full Name</label>
        <input id="fullName" {...register('fullName')} />
        {errors.fullName && <p>{errors.fullName.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email Address</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <p>{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="issueType">Issue Type</label>
        <select id="issueType" {...register('issueType')}>
          <option value="">Select Issue Type</option>
          <option value="bug">Bug Report</option>
          <option value="feature">Feature Request</option>
          <option value="general">General Inquiry</option>
        </select>
        {errors.issueType && <p>{errors.issueType.message}</p>}
      </div>

      <div>
        <label htmlFor="tags">Tags</label>
        <select id="tags" {...register('tags')} multiple>
          <option value="UI">UI</option>
          <option value="Backend">Backend</option>
          <option value="Performance">Performance</option>
        </select>
        {errors.tags && <p>{errors.tags.message}</p>}
      </div>

      <div className="steps-container">
        <label htmlFor="steps">Steps to Reproduce</label>

        <div className="step-item">
          <input id="Step 1" {...register('steps.0')} placeholder="Step 1" />
          {errors.steps?.[0] && <p>{errors.steps[0].message}</p>}
        </div>

        {fields.slice(1).map((field, index) => (
          <div key={field.id} className="step-item">
            <input
              id={`steps-${index + 1}`}
              {...register(`steps.${index + 1}`)}
              placeholder={`Step ${index + 2}`}
            />
            {errors.steps?.[index + 1] && (
              <p>{errors.steps[index + 1].message}</p>
            )}
            <button
              type="button"
              onClick={() => remove(index + 1)}
              className="remove-btn"
            >
              <FaTimes />
            </button>
          </div>
        ))}

        {isLastStepFilled && (
          <button
            type="button"
            onClick={handleAddStep}
            className="plus-btn"
            data-testid="button"
          >
            <FaPlus />
          </button>
        )}
      </div>

      <button type="submit" disabled={!token}>
        {token ? 'Submit' : 'You must be logged in to submit'}
      </button>
    </form>
  );
};

export default SupportRequestForm;
