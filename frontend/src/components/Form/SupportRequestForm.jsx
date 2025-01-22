import React, { useEffect, useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { supportRequestSchema } from './validationSchema';
import { useDispatch } from 'react-redux';
import { saveFormData } from '../../redux/slices/formSlice';
import { useNavigate } from 'react-router-dom';
import { FaPlus, FaTimes } from 'react-icons/fa';
import { useSelector } from 'react-redux';
import axios from 'axios';
import '../../styles/form.css';

const SupportRequestForm = () => {
  const [tags, setTags] = useState([]);

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
      tagId: '',
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

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('http://localhost:8000/v1/tags/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTags(response.data);
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };

    fetchTags();
  }, [token]);

  const onSubmit = async (data) => {
    try {
      await axios.post('http://localhost:8000/v1/support_requests', data, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      dispatch(saveFormData(data));
      navigate('/confirmation');
    } catch (error) {
      console.error('Error submitting form:', error);
    }
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
        <label htmlFor="tagId">Tags</label>
        <select id="tagId" {...register('tagId')}>
          <option value="">Select a Tag</option>
          {tags.map((tag) => (
            <option key={tag.id} value={tag.id}>
              {tag.name}
            </option>
          ))}
        </select>
        {errors.tagId && <p>{errors.tagId.message}</p>}
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
