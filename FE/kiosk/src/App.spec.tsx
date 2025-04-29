describe('<App />', () => {
  it('renders', () => {
    cy.visit('/');
    cy.get('h1').should('exist');
  });
});
