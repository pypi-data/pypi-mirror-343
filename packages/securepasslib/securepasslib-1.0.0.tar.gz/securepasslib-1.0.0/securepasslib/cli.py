import click
from .generator import PasswordGenerator
from .breach_checker import BreachChecker
from .validator import Validator

@click.group()
def cli():
    """SecurePassLib CLI"""
    pass

@cli.command()
@click.option('--length', default=12, help='Length of random password.')
@click.option('--use-upper/--no-use-upper', default=True, help='Include uppercase letters?')
@click.option('--use-digits/--no-use-digits', default=True, help='Include digits?')
@click.option('--use-special/--no-use-special', default=True, help='Include special characters?')
def random(length, use_upper, use_digits, use_special):
    """Generate a random secure password."""
    generator = PasswordGenerator()
    pwd = generator.generate_random_password(length=length, use_upper=use_upper, use_digits=use_digits, use_special=use_special)
    click.echo(pwd)

@cli.command()
@click.option('--template-name', default=None, help='Template name from predefined templates.')
@click.option('--custom-template', default=None, help='Your own custom template string.')
@click.option('--word-length', default=5, help='Word length for W character.')
def template(template_name, custom_template, word_length):
    """Generate a password using a template."""
    generator = PasswordGenerator()
    pwd = generator.generate_by_template(template_name=template_name, custom_template=custom_template, word_length=word_length)
    click.echo(pwd)
    
@cli.command(name="breach-check")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help='Password to check for breaches.')
def breach_check(password):
    """Check if the password has been exposed in a data breach."""
    click.echo("Checking password against breach database...")
    try:
        breached = BreachChecker.is_breached(password)
        if breached:
            click.secho("⚠️  This password has been found in data breaches. Please choose a different one!", fg="red")
        else:
            click.secho("✅ This password was NOT found in any known data breaches.", fg="green")
    except Exception as e:
        click.secho(f"Error checking password breach: {str(e)}", fg="red")
        
@cli.command(name="analyze")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help='Password to analyze.')
def analyze(password):
    """Analyze password strength, entropy, and suggestions."""
    validator = Validator()
    report = validator.get_password_report(password)

    click.echo("\nPassword Analysis:")
    click.echo(f"- Strength: {report['strength_text']} (Score: {report['strength_score']}/6)")
    click.echo(f"- Entropy: {report['entropy_bits']} bits")

    if report['errors']:
        click.secho("- Validation Errors:", fg="red")
        for error in report['errors']:
            click.echo(f"  - {error}")
    else:
        click.secho("- Passed validation.", fg="green")

    if report['suggestions']:
        click.secho("- Suggestions for improvement:", fg="yellow")
        for suggestion in report['suggestions']:
            click.echo(f"  - {suggestion}")

if __name__ == "__main__":
    cli()
