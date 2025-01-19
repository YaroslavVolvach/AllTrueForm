import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import formReducer from '../redux/slices/formSlice';
import SupportRequestForm from '../components/Form/SupportRequestForm';
import userEvent from '@testing-library/user-event';

describe('SupportRequestForm Component', () => {
  let store;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        form: formReducer,
      },
    });
  });

  test('updates store on valid submission with steps', async () => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <SupportRequestForm />
        </MemoryRouter>
      </Provider>
    );

    await userEvent.type(screen.getByLabelText(/Full Name/i), 'John Doe');
    await userEvent.type(
      screen.getByLabelText(/Email Address/i),
      'john.doe@example.com'
    );
    await userEvent.selectOptions(screen.getByLabelText(/Issue Type/i), 'bug');
    await userEvent.selectOptions(screen.getByLabelText(/Tags/i), 'UI');

    await userEvent.type(screen.getByPlaceholderText(/Step 1/i), 'first');

    const plusButton = screen.getByTestId('button', { name: /plus/i });
    expect(plusButton).toBeInTheDocument();

    await userEvent.click(plusButton);

    await userEvent.type(screen.getByPlaceholderText(/Step 2/i), 'second');

    await userEvent.click(screen.getByText(/Submit/i));

    await waitFor(() => {
      const state = store.getState();
      expect(state.form.formData).toEqual({
        fullName: 'John Doe',
        email: 'john.doe@example.com',
        issueType: 'bug',
        tags: ['UI'],
        steps: ['first', 'second'],
      });
    });
  });
});
