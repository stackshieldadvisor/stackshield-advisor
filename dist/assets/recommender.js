
(function () {
  const form = document.getElementById('stack-recommender');
  const output = document.getElementById('recommendation-output');
  if (!form || !output) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    const size = data.get('size');
    const risk = data.get('risk');
    const it = data.get('it');

    const recommendations = [];
    recommendations.push('Password manager with enforced MFA for administrators');
    recommendations.push('Cloud backup with tested restore workflow');

    if (risk === 'ransomware') {
      recommendations.push('Immutable or tamper-resistant backup retention');
      recommendations.push('Documented ransomware recovery runbook');
    }
    if (risk === 'phishing') {
      recommendations.push('Email security / anti-phishing layer');
      recommendations.push('Security awareness training for staff');
    }
    if (risk === 'compliance') {
      recommendations.push('Basic asset inventory and supplier security documentation');
      recommendations.push('Policy templates for access control, backup and incident escalation');
    }
    if (size === 'growing' || it === 'team') {
      recommendations.push('Endpoint protection with central management');
      recommendations.push('Role-based access and admin activity logging');
    }
    if (it === 'none') {
      recommendations.push('Consider a managed service provider for setup and recovery testing');
    }

    output.hidden = false;
    output.innerHTML = '<h2>Recommended first evaluation stack</h2><ol>' + recommendations.map(item => '<li>' + item + '</li>').join('') + '</ol><p><strong>Next:</strong> compare vendors only after these requirements are clear. This is informational guidance, not incident-response or legal advice.</p>';
  });
})();
